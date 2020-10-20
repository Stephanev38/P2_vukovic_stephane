import csv
import requests
import urllib3
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/catalogue/tipping-point-for-planet-earth-how-close-are-we-to-the-edge_643/index.html"

reponse = requests.get(url) #récupération de la page
page = reponse.content
soup = BeautifulSoup(page, "html.parser")

product_page_url = url
print("Product page url", url) #impression de l'url de la page

"""trs = soup.findAll('tr')
[print(str(tr) + '\n\n') for tr in trs]""" #impression des lignes du tableau du site
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

div = soup.find('div', {'id': 'product_description'})
p = div.findNext('p')
print("Product description : ", p.text)

th = table.find('th', text='Product Type')
td = th.findNext('td')
print(th.text, '=', td.text)

th = table.find('th', text='Number of reviews')
td = th.findNext('td')
print(th.text, '=', td.text)

div = soup.find('div', {'class': 'item active'})
img_tags = div.findNext('img')['src']
print("Image url : http://books.toscape.com" + img_tags[5:])

"""with open('fichier.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(fichieriterable)"""



"""print(soup)"""