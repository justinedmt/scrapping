# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 15:33:41 2024

@author: Desmedt
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

# Lire le fichier CSV avec les liens LinkedIn et les noms complets
df = pd.read_csv('data_linkedin_short.csv')

# Définir une fonction pour scraper une page LinkedIn
def scrape_linkedin(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Récupérer les deux premières expériences professionnelles
        experiences = soup.find_all('li', {'class': 'experience-item'}, limit=2)
        
        # Initialiser les variables pour stocker les expériences
        experience_titles = []
        
        for exp in experiences:
            title = exp.find('span', {'class': 'experience-item__title'}).text.strip() if exp.find('span', {'class': 'experience-item__title'}) else None
            experience_titles.append(title)
        
        # Si moins de deux expériences, compléter avec None
        while len(experience_titles) < 2:
            experience_titles.append(None)
        
        return {
            'experience_1': experience_titles[0],
            'experience_2': experience_titles[1]
        }
    else:
        return None

# Créer une liste pour stocker les résultats
results = []

# Scraper chaque URL LinkedIn
for index, row in df.iterrows():
    linkedin_data = scrape_linkedin(row['ct_linkedinurl'])
    if linkedin_data:
        results.append({
            'fullname': row['fullname'],
            'experience_1': linkedin_data['experience_1'],
            'experience_2': linkedin_data['experience_2']
        })

# Convertir les résultats en DataFrame et les enregistrer dans un fichier CSV
results_df = pd.DataFrame(results)
results_df.to_csv('linkedin_data.csv', index=False)

print('Scraping terminé. Les données sont enregistrées dans linkedin_data.csv.')
