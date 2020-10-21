import csv
import requests
import urllib3
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/catalogue/category/books/science_22/index.html"

reponse = requests.get(url) #récupération de la page
page = reponse.content
soup = BeautifulSoup(page, "html.parser")

links = [] #création d'une liste
soup = BeautifulSoup(reponse.text, "html.parser")
urls = soup.findAll('h3')
for h3 in urls:
    a = h3.find('a')
    link = a['href']
    links.append('http://books.toscrape.com/catalogue' + link[8:]) #concaténation du lien de la page avec celui du livre moins 8 caractères (../../..)
print(links)

for link in links:
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    url_product = link
    product_page_url = url_product
    col1 = product_page_url
    print("Product page url", url_product) #impression de l'url de la page

    table = soup.find('table', {'class': 'table table-striped'})
    th = table.find('th', text='UPC')
    td = th.findNext('td')
    col2 = td
    print(th.text, '=', td.text)

    title = soup.find('title')
    col3 = title
    print(title.text[:-28]) #impression du titre

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



