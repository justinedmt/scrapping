# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 08:45:26 2024

@author: Desmedt
"""

#importation des packages nécessaire
import pandas as pd
import re #le mdoule re est pour les expression régulière
import urllib.parse  #ce module permet de décoder les URL encodées

# on charge le fichier csv dans une Dataframe
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


# fonction qui permet de décoder les email (mailto) encodée
def decoder_email(mailto_link):
    if isinstance(mailto_link, str) and mailto_link.startswith('mailto:'):  #verifier si email=string et que le lien commence bien par mailto 
        # Extraire la partie encodée après le mot mailto
        encoded_email = mailto_link[len('mailto:'):]
        # Décoder l'URL encodée a l'aide du module urllib.parse
        decoded_email = urllib.parse.unquote(encoded_email)
        return decoded_email
    return mailto_link




# Appliquer la fonction extraire_adresse à la colonne adresse
df[['Rue', 'CP', 'Ville']] = df['Adresse'].apply(lambda x: pd.Series(extraire_adresse(x)))
#Appliquer la fonction extraire_telephones a la colonne telephones
df[['Telephone1', 'Telephone2']] = df['Téléphones'].apply(lambda x: pd.Series(extraire_telephones(x)))
# Appliquer la fonction decoder_email à la colonne email
df['Email'] = df['Email'].apply(decoder_email)

#on supprimer les anciennes colonnes
df = df.drop(['Adresse', 'Téléphones'], axis=1)

# on enregistre la Dataframe dans un nouveau fichier csv
df.to_csv('info_expert_clean.csv', sep=',', index=False)








