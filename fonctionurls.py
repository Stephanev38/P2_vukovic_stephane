import requests
from bs4 import BeautifulSoup

def getAndParseURL(URL):
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    return(soup)

def getBooksURLs(url):
    soup = getAndParseURL(url)
    return(["/".join(url.split("/")[:-1]) + "/" + x.div.a.get('href') for x in soup.find_all("article", {'class': "product_pod"})])
