# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 08:45:26 2024

@author: Desmedt
"""

#importation des packages nécessaire
import pandas as pd
import re # le module re est pour les expressions régulières
import urllib.parse  # ce module permet de décoder les URL encodées

# on charge le fichier csv dans une DataFrame
df = pd.read_csv('info_expert_judiciaire.csv', delimiter=',')

# fonction qui permet de diviser l'adresse en 3 colonnes différentes (rue, code postal et ville)
def extraire_adresse(adresse):
    if isinstance(adresse, str):  # vérifier si adresse=string
        # expression régulière qui permet la correspondance à une séquence de caractères suivie d'un code postal à cinq chiffres et d'un espace, suivi de la ville.
        match = re.match(r'(.+?)\s*(\d{5})\s+(.+)', adresse) 
        # la méthode match() : Détermine si la RE correspond dès le début de la chaîne.
        # \d expression numérique
        if match:
            return match.groups()
    return (adresse, None, None)  

# fonction qui permet de diviser le numéro de téléphone en deux colonnes pour ceux qui en ont deux 
def extraire_telephones(telephone):
    if isinstance(telephone, str):  # Vérifier si le téléphone = string
        # Diviser les numéros de téléphone par la barre oblique /
        telephones = telephone.split(' / ')
        # Retourner le premier et le deuxième numéro, ou None si pas de deuxième numéro
        return (telephones[0], telephones[1] if len(telephones) > 1 else None)
    return (telephone, None)

# fonction qui permet de décoder les email (mailto) encodées
def decoder_email(mailto_link):
    if isinstance(mailto_link, str) and mailto_link.startswith('mailto:'):  # vérifier si email=string et que le lien commence bien par mailto 
        # Extraire la partie encodée après le mot mailto
        encoded_email = mailto_link[len('mailto:'):]
        # Décoder l'URL encodée à l'aide du module urllib.parse
        decoded_email = urllib.parse.unquote(encoded_email)
        return decoded_email
    return mailto_link

# fonction qui permet de séparer les différentes spécialités en plusieurs colonnes 
def extraire_specialites(specialites):
    if isinstance(specialites, str):  # Vérifier si les spécialités=string
        # Utilise une regex pour capturer les codes de spécialité (exemple X.00.00 ou X.00 ou X.00.00.00 , etc...)
        pattern = re.compile(r'[A-Z]\.\d{2}(?:\.\d{2})*')
        matches = pattern.finditer(specialites)
        
        specialities_list = []
        previous_index = 0
        for match in matches:
            if match.start() > previous_index:
                specialities_list.append(specialites[previous_index:match.start()].strip())
            previous_index = match.start()
        specialities_list.append(specialites[previous_index:].strip())
        
        return specialities_list
    return []

# Appliquer la fonction extraire_adresse à la colonne adresse
df[['Rue', 'CP', 'Ville']] = df['Adresse'].apply(lambda x: pd.Series(extraire_adresse(x)))
# Appliquer la fonction extraire_telephones à la colonne téléphones
df[['Telephone1', 'Telephone2']] = df['Téléphones'].apply(lambda x: pd.Series(extraire_telephones(x)))
# Appliquer la fonction decoder_email à la colonne email
df['Email'] = df['Email'].apply(decoder_email)
# Appliquer la fonction à la colonne des spécialités
specialites_split = df['Spécialités'].apply(extraire_specialites)

# Trouver le nombre maximal de spécialités
max_specialites = specialites_split.apply(len).max()

# créer le nombres de colonne nécessaire pour chaque spécialité
for i in range(max_specialites):
    df[f'Spécialité_{i+1}'] = specialites_split.apply(lambda x: x[i] if i < len(x) else None)

# Supprimer les anciennes colonnes
df = df.drop(['Adresse', 'Téléphones', 'Spécialités'], axis=1)

# Enregistrer la DataFrame dans un nouveau fichier csv
df.to_csv('info_expert_judiciaire_clean.csv', sep=',', index=False)
