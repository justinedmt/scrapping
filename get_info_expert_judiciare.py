# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 11:35:20 2024

@author: Desmedt
"""
# Importation des bibliothèques nécessaires
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

#Charge le fichier csv avec les noms des experts et les liens de leur fiche 
urls_df = pd.read_csv('nom_liens_cncej.csv')

#on configue le driver chrome
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)


#Liste vide pour les variables qu'on veut récupérer pour pouvoir les stcoker
names = []
compagnies = []
adresses = []
telephones = []
emails = []
specialites = []
tribunaux = []

# Fonction pour extraire les informations d'une page
def extract_info(url):
    # Accéder à l'URL fournie
    driver.get(url)
    time.sleep(2)  
    # Obtenir le HTML de la page
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Initialiser les variables à None pour les cas où les données ne sont pas trouvées
    compagnie = None
    adresse = None
    telephone = None
    email = None
    specialites = None
    tribunal = None
    
    # Extraire les informations si elles sont présentes
    compagnie_tag = soup.find('td', string='Compagnie :')
    if compagnie_tag:
        compagnie = compagnie_tag.find_next('td').get_text(strip=True)

    adresse_tag = soup.find('td', string='Adresse :')
    if adresse_tag:
        adresse = adresse_tag.find_next('td').get_text(strip=True)

    telephone_tag = soup.find('td', string='Téléphones :')
    if telephone_tag:
        telephone = telephone_tag.find_next('td').get_text(strip=True)
        
    email_tag = soup.find('td', string='Email :')
    if email_tag:
        email_link = email_tag.find_next('td').find('a')
        email = email_link['href'] if email_link else 'N/A'  

    specialites_tag = soup.find('td', string='Spécialités :')
    if specialites_tag:
        specialites = specialites_tag.find_next('td').get_text(strip=True)

    tribunal_tag = soup.find('td', string='Tribunal :')
    if tribunal_tag:
        tribunal = tribunal_tag.find_next('td').get_text(strip=True)

    # Retourner un dictionnaire avec les informations extraites
    return {
        'Compagnie': compagnie,
        'Adresse': adresse,
        'Téléphones': telephone,
        'Email': email,
        'Spécialités': specialites,
        'Tribunal': tribunal,
    }


# Parcourir chaque ligne du DataFrame (données du fichier csv)
for index, row in urls_df.iterrows():
    name = row['Nom']
    url = row['Lien']
    
    try:
        # Extraire les informations de l'URL
        info = extract_info(url)
        # Ajouter les informations extraites aux listes correspondantes
        names.append(name)
        compagnies.append(info['Compagnie'])
        adresses.append(info['Adresse'])
        telephones.append(info['Téléphones'])
        emails.append(info['Email'])
        specialites.append(info['Spécialités'])
        tribunaux.append(info['Tribunal'])
    except Exception as e:
        #affiche un message d'erreur en cas de problème lors de l'extraction des informations
        print(f"Erreur lors de l'extraction des informations pour {name} à l'URL {url}: {e}")

# Créer un DataFrame avec les informations extraites
data = {
    'Nom': names,
    'Compagnie': compagnies,
    'Adresse': adresses,
    'Téléphones': telephones,
    'Email': emails,
    'Spécialités': specialites,
    'Tribunal': tribunaux,
}


#Extraire info dans un fichier csv
df = pd.DataFrame(data)
df.to_csv('info_expert_judiciaire.csv', index=False, encoding='utf-8')
#fermer le driver
driver.quit()

    


