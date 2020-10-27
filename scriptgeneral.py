# -*-coding:utf8 -*

import os
import csv
import requests
import urllib3
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/"

response = requests.get(url) # récupération de la page à analyser
response.encoding = "utf-8"
soup = BeautifulSoup(response.text, "html.parser")

uls = []
url = []
response.encoding = "utf-8"
soup = BeautifulSoup(response.text, "html.parser")
uls = soup.find('ul', {'class': 'nav nav-list'}).find('ul').find_all('a')

for ul in soup.find_all('a'):
    """a = ul.find_all('a')
    ul = a['href']
    uls.append(ul)"""
    uls.append(ul. get('href'))
    #uls.append('http://books.toscrape.com/' + ul)
print(uls) # url.append('http://books.toscrape.com/' + ul[2:])

#print(url)

for ul in uls:
    response = requests.get(ul)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")
    url_product = ul
    product_page_url = url_product
    print(product_page_url)
    
    table = soup.find('table', {'class': 'table table-striped'})
    th = table.find('th', text='UPC')
    td = th.findNext('td')
    col2 = td
    print(th.text, '=', td.text)
    
    div = soup.find('div', {'class': 'col-sm-6 product_main'})
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
    
    div = soup.find('div', {'id': 'product_description'})
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
    
    div = soup.find('div', {'class': 'item active'})
    img_tags = div.findNext('img')['src']
    col10 = "http://books.toscrape.com" + img_tags[5:]
    print("Image url : http://books.toscrape.com" + img_tags[5:]) #impression de l'url de l'image
"""response = requests.get(url)
page = response.content
soup = BeautifulSoup(page, "html.parser")
response.encoding = "utf-8"
print(soup)"""

