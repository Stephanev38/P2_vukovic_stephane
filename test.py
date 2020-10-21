import csv
import requests
import urllib3
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/catalogue/the-most-perfect-thing-inside-and-outside-a-birds-egg_938/index.html"

reponse = requests.get(url) #récupération de la page
page = reponse.content
soup = BeautifulSoup(page, "html.parser")

product_page_url = url
col1 = product_page_url
print("Product page url", url) #impression de l'url de la page

"""trs = soup.findAll('tr')
[print(str(tr) + '\n\n') for tr in trs]""" #impression des lignes du tableau du site
"""print(len(trs))""" #impression du nombre de lignes

table = soup.find('table', {'class': 'table table-striped'})
th = table.find('th', text='UPC')
td = th.findNext('td')
col2 = td
print(th.text, '=', td.text)

title = soup.find('title')
col3 = title
print(title.text) #impression du titre

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
col7 = p
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
print("Image url : http://books.toscrape.com" + img_tags[5:]) #impression de l'url de l'image
col10 = "http://books.toscrape.com" + img_tags[5:]

file_name = "fichier2.csv"
file = open(file_name, "w")
writer = csv.writer(file)
writer.writerow(("product page url", "universal product code", "title", "price including tax", "price excluding tax", "number available", "product description", "category", "review rating", "image url"))
writer.writerow((col1 , col2.text, col3.text, col4.text, col5.text, col6.text, col7.text, col8.text, col9.text, col10))
file.close()

"""with open('fichier.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(fichieriterable)"""



"""print(soup)"""