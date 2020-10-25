# -*-coding:utf8 -*

import os
import csv
import requests
import urllib3
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/"

contenu = requests.get(url) # récupération de la page à analyser
soup = BeautifulSoup(contenu.text, "html.parser")

links = []
uls = soup.findAll('ul', {'class': 'nav nav-list'})

for ul in uls:
    """a = ul.find('a')
    link = a['href']
    links.append('http://books.toscrape.com/' + link[2:])
    print(links)"""
    a = ul.find('a')
    link = a.find['href']
    links.append('http://books.toscrape.com/' + link[2:])
    print(links)

"""response = requests.get(url)
page = response.content
soup = BeautifulSoup(page, "html.parser")
print(soup)"""

