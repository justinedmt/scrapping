# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 08:45:26 2024

@author: Desmedt
"""

#importation des packages nécessaire
import pandas as pd
import re #le mdoule re est pour les expression régulière

# Charger le fichier csv dans une Dataframe
df = pd.read_csv('info_expert_judiciaire.csv', delimiter=',')

#fonction qui permet de diviser l'adresse en 3 colonne différentes (rue, code postale et ville)
def extraire_adresse(adresse):
    if isinstance(adresse, str): #verifer si adresse=string
        #expression régulière qui permet la correspondance à une séquence de caractères suivie d'un code postal à cinq chiffres et d'un espace, suivi de la ville.
        match = re.match(r'(.+?)\s*(\d{5})\s+(.+)', adresse) 
        #la méthode match() : Détermine si la RE fait correspond dès le début de la chaîne.
        #\d expression numérique
        if match:
            return match.groups()
    return (adresse, None, None)  

# fonction qui permet de diviser le numero de telephone en deux colonne pour ceux qui en ont deux 
def extraire_telephones(telephone):
    if isinstance(telephone, str):  # Vérifier si le téléphone = string
        # Diviser les numéros de téléphone par la barre oblique (/)
        telephones = telephone.split(' / ')
        # Retourner le premier et le deuxième numéro, ou None si pas de deuxième numéro
        return (telephones[0], telephones[1] if len(telephones) > 1 else None)
    return (telephone, None)

# Fonction pour diviser les spécialités en plusieurs lignes
def extraire_specialites(specialites):
    if isinstance(specialites, str):  # Vérifier si les spécialités=string
        # Diviser les spécialités par le motif 'G.xx.xx - '
        specialites_list = re.split(r'(?<=\))', specialites)
        return [s.strip() for s in specialites_list if s.strip()]
    return [specialites]

# Appliquer la fonction extraire_adresse à la colonne adresse
df[['Rue', 'CP', 'Ville']] = df['Adresse'].apply(lambda x: pd.Series(extraire_adresse(x)))
#Appliquer la fonction extraire_telephones a la colonne telephones
df[['Telephone1', 'Telephone2']] = df['Téléphones'].apply(lambda x: pd.Series(extraire_telephones(x)))


# Appliquer la fonction extraire_specialites à la colonne des spécialités
specialites_split = df['Spécialités'].apply(extraire_specialites)
# Exploser les spécialités en plusieurs lignes
df = df.explode('Spécialités')


df = df.drop(['Adresse', 'Téléphones'], axis=1)
# Enregistrer le Dataframe dans un nouveau fichier csv
df.to_csv('info_expert_clean.csv', sep=',', index=False)








