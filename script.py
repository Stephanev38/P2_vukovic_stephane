import csv
import requests
import urllib3
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/catalogue/tipping-point-for-planet-earth-how-close-are-we-to-the-edge_643/index.html"

reponse = requests.get(url) #récupération de la page
page = reponse.content
soup = BeautifulSoup(page, "html.parser")

product_page_url = url
print(url) #impression de l'url de la page

trs = soup.findAll('tr')
[print(str(tr) + '\n\n') for tr in trs] #impression des lignes du tableau du site
"""print(len(trs))""" #impression du nombre de lignes
table = soup.find('table', {'class': 'table table-striped'})
th = table.find('th', text='UPC')
td = th.findNext('td')
print(th.text, '=', td.text)

title = soup.find('title')
print(title.text) #impression du titre

th = table.find('th', text='Price (incl. tax)')
td = th.findNext('td')
print(th.text, '=', td.text)

th = table.find('th', text='Price (excl. tax)')
td = th.findNext('td')
print(th.text, '=', td.text)

th = table.find('th', text='Availability')
td = th.findNext('td')
print(th.text, '=', td.text)

"""article = soup.find('article', {'class': 'product_page'})
p = article.find('p')
print(p.text)"""

"""article = soup.find('article', {'class': 'product_page'})
p = article.find('p')
print(article)"""

"""article = soup.find('p', {'class': 'product_page'})
p = article.findNext('p')
print('product-description = ', p)"""


th = table.find('th', text='Product Type')
td = th.findNext('td')
print(th.text, '=', td.text)

th = table.find('th', text='Number of reviews')
td = th.findNext('td')
print(th.text, '=', td.text)

"""with open('fichier.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(fichieriterable)"""



"""print(soup)"""