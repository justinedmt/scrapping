# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 11:21:17 2024

@author: Desmedt
"""

import pandas as pd

# Charger le fichier CSV dans un DataFrame
df = pd.read_csv('cncej_noms_liens.csv', delimiter='\t')


def modifier_lien(lien):
    return lien.replace('/availability', '?nomenclature=false')


df['Lien'] = df['Lien'].apply(modifier_lien)

df.to_csv('nouveau_fichier.csv', sep='\t', index=False)
