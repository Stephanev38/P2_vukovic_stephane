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
from fonctionprime import fonctionG
from fonctionurls import getAndParseURL
from fonctionurls import getBooksURLs
from fonctioncategories import categoriesAndCsv
from fonctioninformations import informationsAndCsv

def main():
    os.mkdir("images")
    os.mkdir("csv")
    URL = "http://books.toscrape.com/"
    booksUrls = []
    fonctionG(getAndParseURL, getBooksURLs, booksUrls)
    getAndParseURL(URL)
    getBooksURLs(URL)
    categoriesAndCsv(booksUrls)
    informationsAndCsv(booksUrls)

if __name__ == "__main__":
    main()