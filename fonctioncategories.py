from bs4 import BeautifulSoup
import requests
import csv

def categoriesAndCsv(booksUrls):
    for link in booksUrls: # ouverture d'une boucle pour récupérer les catégories des livres et créer les csv avec en-têtes
        response = requests.get(link)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")

        try:
            li = soup.find('li', {'class': 'active'})
            a = li.find_previous('a')
            col8 = a
        except Exception as e:
            print(e)

        with open(col8.text + '.csv', 'w') as out_file: # création des csv avec en-têtes
            csv_writer = csv.writer(out_file)
            csv_writer.writerow(['product page url', 'universal product code', 'title', 'price including tax', 'price excluding tax', 'number available', 'product description', 'category', 'review rating', 'image url'])
