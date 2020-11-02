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

url = "http://books.toscrape.com/"

response = requests.get(url)
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

links = [] #création d'une liste
response.encoding = "utf-8" #encodage
soup = BeautifulSoup(response.text, "html.parser") #variable soup méthode scraping
urls = soup.findAll('h3')  #utilisation varialble soup - 
for h3 in urls:
    a = h3.find('a')
    link = a['href']
    links.append('http://books.toscrape.com/catalogue' + link[8:]) #concaténation du lien de la page avec celui du livre moins 8 caractères (../../..)

with open('category.csv', 'a') as out_file:
    csv_writer = csv.writer(out_file)
    csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])

for link in booksUrls:
    response = requests.get(link)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    try:
        url_product = link
        product_page_url = url_product
        print(product_page_url)
    except Exception as e:
        print(e)
        
    try:
        table = soup.find('table', {'class': 'table table-striped'})
        th = table.find('th', text='UPC')
        td = th.findNext('td')
        col2 = td
        print(th.text, '=', td.text)
    except Exception as e:
        print(e)

    try:    
        div = soup.find('div', {'class': 'col-sm-6 product_main'})
        h1 = div.find('h1')
        print("Title :", h1.text) #impression du titre
    except Exception as e:
        print(e)

    try:
        th = table.find('th', text='Price (incl. tax)')
        td = th.findNext('td')
        col4 = td
        print(th.text, '=', td.text) #impression du prix ttc
    except Exception as e:
        print(e)

    try:
        th = table.find('th', text='Price (excl. tax)')
        td = th.findNext('td')
        col5 = td
        print(th.text, '=', td.text) #impression du prix ht
    except Exception as e:
        print(e)

    try:
        th = table.find('th', text='Availability')
        td = th.findNext('td')
        col6 = td
        print(th.text, '=', td.text) #impression d'availability
    except Exception as e:
        print(e)    

    try:
        div = soup.find('div', {'id': 'product_description'})
        p = div.findNext('p')
        print("Product description : ", p.text) #impression de product description
    except Exception as e:
        print(e)

    try:
        li = soup.find('li', {'class': 'active'})
        a = li.find_previous('a')
        category = a['href']
        col8 = a
        print('Category = ', a.text) #impression de la categorie
    except Exception as e:
        print(e)
        
    try:
        th = table.find('th', text='Number of reviews')
        td = th.findNext('td')
        col9 = td
        print(th.text, '=', td.text) #impression du nombre dans le stock
    except Exception as e:
        print(e)

    try:
        div = soup.find('div', {'class': 'item active'})
        img_tags = div.findNext('img')['src']
        col10 = "http://books.toscrape.com" + img_tags[5:]
        print("Image url : http://books.toscrape.com" + img_tags[5:]) #impression de l'url de l'image
        image_url = col10
        image_filename = wget.download(image_url)
        print('Image Successfully Downloaded: ', image_filename)
    except Exception as e:
        print(e)

    with open('category.csv', 'a') as out_file:
        csv_writer = csv.writer(out_file)
        csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
        out_file.close()

    """if col8.text == "Travel":
        with open('Travel.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Mystery":
        with open('Mystery.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Historical Fiction":
        with open('Historical_Fiction.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Sequential Art":
        with open('Sequential_Art.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Classics":
        with open('Classics.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Philosophy":
        with open('Philosophy.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Romance":
        with open('Romance.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Womens Fiction":
        with open('Womens_Fiction.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Fiction":
        with open('Fiction.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Childrens":
        with open('Childrens.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Religion":
        with open('Religion.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Nonfiction":
        with open('Nonfiction.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Music":
        with open('Music.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Default":
        with open('Default.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Science Fiction":
        with open('Science_Fiction.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Sports and Games":
        with open('Sports_and_Games.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Add a comment":
        with open('Add_a_comment.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Fantasy":
        with open('Fantasy.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "New Adult":
        with open('New_Adult.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Young Adult":
        with open('Young_Adult.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Science":
        with open('Science.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Poetry":
        with open('Poetry.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Paranormal":
        with open('Paranormal.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Art":
        with open('Art.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Psychology":
        with open('Psychology.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Autobiography":
        with open('Autobiography.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Parenting":
        with open('Parenting.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Adult Fiction":
        with open('Adult_Fiction.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Humor":
        with open('Humor.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Horror":
        with open('Horror.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "History":
        with open('History.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Food and Drink":
        with open('Food_and_Drink.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Christian Fiction":
        with open('Christian_Fiction.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Business":
        with open('Business.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Biography":
        with open('Biography.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Thriller":
        with open('Thriller.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Contemporary":
        with open('Contemporary.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Spirituality":
        with open('Spirituality.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Academic":
        with open('Academic.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Self Help":
        with open('Self_Help.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Historical":
        with open('Historical.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Christian":
        with open('Christian.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Suspense":
        with open('Suspense.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Short Stories":
        with open('Short_Stories.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Novels":
        with open('Novels.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Health":
        with open('Health.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Politics":
        with open('Politics.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Cultural":
        with open('Cultural.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Erotica":
        with open('Erotica.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()
    elif col8.text == "Crime":
        with open('Crime.csv', 'a') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
            csv_writer.writerow([product_page_url , col2.text , h1.text, col4.text, col5.text, col6.text, p.text, col8.text, col9.text, col10])
            out_file.close()"""