# -*-coding:utf8 -*

import os
import csv
import requests
import urllib3
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

url = "http://books.toscrape.com/"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

def getAndParseURL(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return(soup)

"""soup.find("article", {'class': "product_pod"})
soup.find("article", {'class': "product_pod"}).div.a
soup.find("article", {'class': "product_pod"}).div.a.get('href')
soup.find("article", {'class': "product_pod"}).div.img.get("alt")"""

page_products_urls = [x.div.a.get('href') for x in soup.find_all("article", {'class': "product_pod"})]

def getBooksURLs(url):
    soup = getAndParseURL(url)
    return(["/".join(url.split("/")[:-1]) + "/" + x.div.a.get('href') for x in soup.find_all("article", {'class': "product_pod"})])

categories_urls = [url + x.get('href') for x in soup.find_all("a", href=re.compile("catalogue/category/books"))]
categories_urls = categories_urls[1:]

pages_urls = [url]

soup = getAndParseURL(pages_urls[0])

while len(soup.find_all('a', href=re.compile("page"))) == 2 or len(pages_urls) == 1:
    new_url = "/".join(pages_urls[-1].split("/")[:-1]) + "/" + soup.find_all('a', href=re.compile("page"))[-1].get("href")
    pages_urls.append(new_url)
    soup = getAndParseURL(new_url)

booksUrls = []
for page in pages_urls:
    booksUrls.extend(getBooksURLs(page))

"""links = [] #création d'une liste"""
response.encoding = "utf-8" #encodage
soup = BeautifulSoup(response.text, "html.parser") #variable soup méthode scraping
"""urls = soup.findAll('h3')  #utilisation varialble soup - 
for h3 in urls:
    a = h3.find('a')
    link = a['href']
    links.append('http://books.toscrape.com/catalogue' + link[8:]) #concaténation du lien de la page avec celui du livre moins 8 caractères (../../..)"""

for link in booksUrls:
    response = requests.get(link)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    try:
        url_product = link
        product_page_url = url_product
        print(product_page_url)
    except:
        print()
        
    try:
        table = soup.find('table', {'class': 'table table-striped'})
        th = table.find('th', text='UPC')
        td = th.findNext('td')
        col2 = td
        print(th.text, '=', td.text)
    except:
        print()

    try:    
        div = soup.find('div', {'class': 'col-sm-6 product_main'})
        h1 = div.find('h1')
        print("Title :", h1.text) #impression du titre
    except:
        print()

    try:
        th = table.find('th', text='Price (incl. tax)')
        td = th.findNext('td')
        col4 = td
        print(th.text, '=', td.text) #impression du prix ttc
    except:
        print()

    try:
        th = table.find('th', text='Price (excl. tax)')
        td = th.findNext('td')
        col5 = td
        print(th.text, '=', td.text) #impression du prix ht
    except:
        print()

    try:
        th = table.find('th', text='Availability')
        td = th.findNext('td')
        col6 = td
        print(th.text, '=', td.text) #impression d'availability
    except:
        print()    

    try:
        div = soup.find('div', {'id': 'product_description'})
        p = div.findNext('p')
        print("Product description : ", p.text) #impression de product description
    except:
        print()

    try:
        li = soup.find('li', {'class': 'active'})
        a = li.find_previous('a')
        category = a['href']
        col8 = a
        print('Category = ', a.text) #impression de la categorie
    except:
        print()
        
    try:
        th = table.find('th', text='Number of reviews')
        td = th.findNext('td')
        col9 = td
        print(th.text, '=', td.text) #impression du nombre dans le stock
    except:
        print()

    try:
        div = soup.find('div', {'class': 'item active'})
        img_tags = div.findNext('img')['src']
        col10 = "http://books.toscrape.com" + img_tags[5:]
        print("Image url : http://books.toscrape.com" + img_tags[5:]) #impression de l'url de l'image
    except:
        print()

    """with open('categorie.csv', 'a') as out_file:
        csv_writer = csv.writer(out_file)
        csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
        csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
        out_file.close()"""