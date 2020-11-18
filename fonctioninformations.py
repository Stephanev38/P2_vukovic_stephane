from bs4 import BeautifulSoup
import requests
import csv
import wget

def informationsAndCsv(booksUrls):
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
