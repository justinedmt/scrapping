# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 09:03:21 2024

@author: Desmedt
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from bs4 import BeautifulSoup

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
url = 'https://www.cncej.org/annuaire'
driver.get(url)
time.sleep(2)

names = []
links = []
base_url = 'https://www.cncej.org/'

def scrape_page():
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.findAll('tr', {'role': 'row'})
    
    new_data_found = False
    
    for row in rows:
        name_cell = row.find('td')
        link_cell = row.find('td', {'class': 'text-center'}).find('a', {'data-remote': 'true'})
        
        if name_cell and link_cell:
            name = name_cell.text.strip()
            link = base_url + link_cell['href']
            
            if name not in names and link not in links:
                names.append(name)
                links.append(link)
                new_data_found = True
    
    return new_data_found

try:
    while True:
        new_data = scrape_page()
        
        if not new_data:
            print("No new data found. Stopping the scraper.")
            break
        
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

data = {'Nom': names, 'Lien': links}
df = pd.DataFrame(data)
df.to_csv('cncej_noms_liens.csv', index=False, encoding='utf-8')

driver.quit()
