# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 11:35:20 2024

@author: Desmedt
"""

#importation des packages nécessaire pour le code 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from bs4 import BeautifulSoup
import random

# Configurer le driver chrome
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# URL du site qu'on veut scrapper ici le site des experts judiciaires CNCEJ
url = 'https://www.cncej.org/annuaire'
driver.get(url)

# Attendre un intervalle de temps aléatoire pour éviter d'être détecté comme un robot
sleep_time = random.uniform(1, 10)  
time.sleep(sleep_time)

# On initialise des listes vides de nos variables pour pouvoir les stocker
names = []
links = []
# Cette variable nous permettra d'ajouter ce lien devant le lien scrappé pour qu'il puisse marcher
base_url = 'https://www.cncej.org/'

# Fonction pour le scrapping
def scrape_page():
    # Obtenir le HTML de la page actuelle
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # Trouver toutes les lignes du tableau contenant les données des experts
    rows = soup.findAll('tr', {'role': 'row'})
    
    new_data_found = False
    
    # Parcourir chaque ligne du tableau
    for row in rows:
        name_cell = row.find('td')
        if name_cell:
            # Trouver la cellule contenant le lien
            link_cell = row.find('td', {'class': 'text-center'})
            if link_cell:
                # Trouver le tag <a> avec l'attribut data-remote
                link_tag = link_cell.find('a', {'data-remote': 'true'})
                if link_tag:
                    # Extraire le nom et le lien de l'expert
                    name = name_cell.text.strip()
                    link = base_url + link_tag['href']
                    
                    # Vérifier si le nom et le lien n'ont pas déjà été ajoutés
                    if name not in names and link not in links:
                        # Ajouter le nom et le lien aux listes
                        names.append(name)
                        links.append(link)
                        new_data_found = True
                else:
                    print("Lien non trouvé dans cette cellule : ", link_cell)
            else:
                print("Cellule de lien non trouvée dans cette ligne : ", row)
        else:
            print("Cellule de nom non trouvée dans cette ligne : ", row)
    
    return new_data_found

try:
    while True:
        # Scraper les données de la page
        new_data = scrape_page()
        
        # Si aucune nouvelle donnée n'est trouvée, arrêter le scraping
        if not new_data:
            print("Pas de nouvelles données = scraping stop.")
            break
        
        # Essayer de cliquer sur le bouton "Suivant" pour passer à la page suivante
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Suivante')]"))
            )
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(2)  
        except Exception as e:
            print("Le bouton 'Suivant' n'existe plus : ", e)
            break

except Exception as e:
    print("Une erreur s'est produite : ", e)

# On ajoute les données récoltées et on les récupère dans un fichier csv
data = {'Nom': names, 'Lien': links}
df = pd.DataFrame(data)
df.to_csv('cncej_noms_lien.csv', index=False, encoding='utf-8')
#fermer le driver
driver.quit()
