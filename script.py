# -*-coding:utf8 -*

import os
import csv
import requests
import urllib3
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html"

contenu = requests.get(url) # récupération de la page à analyser
page = BeautifulSoup(contenu.text, "html.parser")

product_page_url = url
print(url)

table = page.find('table', {'class': 'table table-striped'})
th = table.find('th', text='UPC')
td = th.findNext('td')
col2 = td
print(th.text, '=', td.text)

div = page.find('div', {'class': 'col-sm-6 product_main'})
h1 = div.find('h1')
print("Title :", h1.text) #impression du titre

th = table.find('th', text='Price (incl. tax)')
td = th.findNext('td')
col4 = td
print(th.text, '=', td.text) #impression du prix ttc

th = table.find('th', text='Price (excl. tax)')
td = th.findNext('td')
col5 = td
print(th.text, '=', td.text) #impression du prix ht

th = table.find('th', text='Availability')
td = th.findNext('td')
col6 = td
print(th.text, '=', td.text) #impression d'availability

div = page.find('div', {'id': 'product_description'})
p = div.findNext('p')
print("Product description : ", p.text) #impression de product description

th = table.find('th', text='Product Type')
td = th.findNext('td')
col8 = td
print(th.text, '=', td.text) #impression de la categorie

th = table.find('th', text='Number of reviews')
td = th.findNext('td')
col9 = td
print(th.text, '=', td.text) #impression du nombre dans le stock

div = page.find('div', {'class': 'item active'})
img_tags = div.findNext('img')['src']
col10 = "http://books.toscrape.com" + img_tags[5:]
print("Image url : http://books.toscrape.com" + img_tags[5:]) #impression de l'url de l'image

with open('fichier.csv', 'wt') as out_file:
    csv_writer = csv.writer(out_file, delimiter='\t')
    csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
    csv_writer.writerow([product_page_url, col2.text, h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])