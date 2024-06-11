# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 11:54:12 2024

@author: Desmedt
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Charger les URLs depuis le fichier CSV
urls_df = pd.read_csv('cncej_noms_liens.csv')
infos_expert = []

for url in urls_df['Lien']:
    driver.get(url)
    time.sleep(2)  
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    
    company = soup.find('table', class_='member-show').find('tbody').find_all('tr')[0].find('p').text.strip()
    address = soup.find('table', class_='member-show').find('tbody').find_all('tr')[2].find('p').text.strip()
    telephone = soup.find('table', class_='member-show').find('tbody').find_all('tr')[3].find('p').text.strip()
    email = soup.find('table', class_='member-show').find('tbody').find_all('tr')[4].find('a')['href'].split(':')[-1]
    court_info = soup.find('table', class_='member-show').find('tbody').find_all('tr')[6:]
    status = court_info[0].find('p').text.strip()
    specialties = [spec.text.strip() for spec in court_info[1].find('p').find_all('br')]
    tribunal = court_info[2].find('p').text.strip()
    inscription_year = court_info[3].find('p').text.strip()
    
    infos_expert.append({
        'Company': company,
        'Address': address,
        'Telephone': telephone,
        'Email': email,
        'Status': status,
        'Specialties': ', '.join(specialties),
        'Tribunal': tribunal,
        'Inscription Year': inscription_year
    })


driver.quit()
df = pd.DataFrame(infos_expert)
df.to_csv('expert_info.csv', index=False)

print("Les informations ont été sauvegardées dans le fichier .csv.")
