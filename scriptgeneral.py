# -*-coding:utf8 -*

import os
import csv
import requests
import urllib3
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
import urllib.request
import wget

def main():
    pass

URL = "http://books.toscrape.com/"

response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

def getAndParseURL(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return(soup)

soup.find("article", {'class': "product_pod"})
soup.find("article", {'class': "product_pod"}).div.a
soup.find("article", {'class': "product_pod"}).div.a.get('href')
soup.find("article", {'class': "product_pod"}).div.img.get("alt")

page_products_urls = [x.div.a.get('href') for x in soup.find_all("article", {'class': "product_pod"})]

def getBooksURLs(url):
    soup = getAndParseURL(url)
    return(["/".join(url.split("/")[:-1]) + "/" + x.div.a.get('href') for x in soup.find_all("article", {'class': "product_pod"})])

categories_urls = [URL + x.get('href') for x in soup.find_all("a", href=re.compile("catalogue/category/books"))]
categories_urls = categories_urls[1:]

pages_urls = [URL]

soup = getAndParseURL(pages_urls[0])

while len(soup.find_all('a', href=re.compile("page"))) == 2 or len(pages_urls) == 1:
    new_url = "/".join(pages_urls[-1].split("/")[:-1]) + "/" + soup.find_all('a', href=re.compile("page"))[-1].get("href")
    pages_urls.append(new_url)
    soup = getAndParseURL(new_url)

booksUrls = []
for page in pages_urls:
    booksUrls.extend(getBooksURLs(page))

links = [] #création d'une liste
response.encoding = "utf-8" #encodage
soup = BeautifulSoup(response.text, "html.parser") #variable soup méthode scraping
urls = soup.findAll('h3')  #utilisation varialble soup - 
for h3 in urls:
    a = h3.find('a')
    link = a['href']
    links.append('http://books.toscrape.com/catalogue' + link[8:]) #concaténation du lien de la page avec celui du livre moins 8 caractères (../../..)

def categoriesAndCsv():
    for link in booksUrls: # ouverture d'une boucle pour récupérer les catégories des livres et créer les csv avec en-têtes
        response = requests.get(link)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")

        try:
            li = soup.find('li', {'class': 'active'})
            a = li.find_previous('a')
            #category = a['href']
            col8 = a
        except Exception as e:
            print(e)

        with open(col8.text + '.csv', 'w') as out_file: # création des csv avec en-têtes
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])

categoriesAndCsv()

def informationsAndCsv():
    for link in booksUrls: # boucle permettant de récupérer les informations de tous les livres
        response = requests.get(link)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")

        try:
            url_product = link # lien de la page du livre
            product_page_url = url_product
            print(product_page_url)
        except Exception as e:
            print(e)
            
        try:
            table = soup.find('table', {'class': 'table table-striped'}) # le code universel du livre
            th = table.find('th', text='UPC')
            td = th.findNext('td')
            col2 = td
            print(th.text, '=', td.text)
        except Exception as e:
            print(e)

        try:    
            div = soup.find('div', {'class': 'col-sm-6 product_main'}) # titre du livre
            h1 = div.find('h1')
            print("Title :", h1.text)
        except Exception as e:
            print(e)

        try:
            th = table.find('th', text='Price (incl. tax)') # prix ttc du livre
            td = th.findNext('td')
            col4 = td
            print(th.text, '=', td.text)
        except Exception as e:
            print(e)

        try:
            th = table.find('th', text='Price (excl. tax)') # prix ht du livre
            td = th.findNext('td')
            col5 = td
            print(th.text, '=', td.text)
        except Exception as e:
            print(e)

        try:
            th = table.find('th', text='Availability') # availability
            td = th.findNext('td')
            col6 = td
            print(th.text, '=', td.text)
        except Exception as e:
            print(e)    

        try:
            div = soup.find('div', {'id': 'product_description'}) # description du livre
            p = div.findNext('p')
            print("Product description : ", p.text)
        except Exception as e:
            print(e)

        try:
            li = soup.find('li', {'class': 'active'}) # catégorie d'appartenance du livre
            a = li.find_previous('a')
            #category = a['href']
            col8 = a
            print('Category = ', a.text)
        except Exception as e:
            print(e)

        try:
            th = table.find('th', text='Number of reviews') # quantité du stock du livre
            td = th.findNext('td')
            col9 = td
            print(th.text, '=', td.text)
        except Exception as e:
            print(e)

        try:
            div = soup.find('div', {'class': 'item active'}) # url de l'image d'illustartion du livre
            img_tags = div.findNext('img')['src']
            col10 = "http://books.toscrape.com" + img_tags[5:]
            print("Image url : http://books.toscrape.com" + img_tags[5:])
            image_url = col10
            image_filename = wget.download(image_url, "images/" + h1.text)
            print('Image Successfully Downloaded: ', image_filename)
        except Exception as e:
            print(e)

        with open(col8.text + '.csv', 'a') as out_file: # complément du csv avec les informations du livre
            csv_writer = csv.writer(out_file)
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()

informationsAndCsv()

if __name__ == "__main__":
    main()