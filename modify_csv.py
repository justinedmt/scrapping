# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 11:21:17 2024

@author: Desmedt
"""

#importation du apckagfe
import pandas as pd

# Charger le fichier CSV dans un DataFrame
df = pd.read_csv('cncej_noms_liens.csv', delimiter=',')

#fonction pour modifier les liens
def modifier_lien(lien):
    return lien.replace('/availability', '?nomenclature=false')

#Appliquer la fonction a la colonne Lien
df['Lien'] = df['Lien'].apply(modifier_lien)
#Enregistrer le Dataframe modifié dans un nouveau fichier csv
df.to_csv('nouveau_fichier.csv', sep=',', index=False)

