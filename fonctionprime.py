import requests
from bs4 import BeautifulSoup
import re

def fonctionG(getAndParseURL, getBooksURLs, booksUrls):
    URL = "http://books.toscrape.com/"
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    pages_urls = [URL]
    soup = getAndParseURL(pages_urls[0])
    
    while len(soup.find_all('a', href=re.compile("page"))) == 2 or len(pages_urls) == 1:
        new_url = "/".join(pages_urls[-1].split("/")[:-1]) + "/" + soup.find_all('a', href=re.compile("page"))[-1].get("href")
        pages_urls.append(new_url)
        soup = getAndParseURL(new_url)

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
