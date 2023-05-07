#!/usr/bin/env python
import re
from requests import get
from bs4 import BeautifulSoup
import json
from elasticsearch import Elasticsearch
from os import path
import time
import csv



def index_json(bs):

    category = bs.find('div', {'class': 'datos-articulo'}).findAll('h3')[0].string.split(". ")
    title = bs.find('li', {'class': 'tituloArticulo'}).string

    if bs.find('li', {'class': 'autoresArticulo'}):
        name = bs.find('li', {'class': 'autoresArticulo'}).string.split(", ")
        author = name[1] + " " + name[0]
    else:
        author = "RACMYP"

    pdf_link = bs.find('li', {'class': 'puntoPDF2'}).findAll('a', href=re.compile("abrir_pdf.php"))[0].get('href')
    id = pdf_link.split("=")[1]
    year = id.split("-")[2]
    code = id.split("-")[3]
    fascicle = code[0]
    start_page = code[1:6]
    end_page = code[6:11]

    metadata_json = {
        'id': id,
        'category': category[0],
        'title': title,
        'author': author,
        'fascicle': fascicle,
        'year': year,
        'start_page': start_page,
        'end_page': end_page,
        'pdf_link': pdf_link
    }

    #TODO ALL PDF's Download - index in ES

    content = get("https://www.boe.es/biblioteca_juridica/anuarios_derecho/"+pdf_link)
    if content.status_code == 200 and content.headers['content-type'] == 'application/pdf':
        with open(path.join('./articles_pdf/', id+'.pdf'), 'wb') as pdf:
            pdf.write(content.content)
    #    es.index(index="racmyp_articles", body=metadata_json)

    print(metadata_json)

    return [id, category, title, author, fascicle, year, start_page, end_page, pdf_link]

def sracpping_article(link):
    extension = link.get('href')
    url = "https://www.boe.es/biblioteca_juridica/anuarios_derecho/" + extension
    article_view = get(url)
    bs_article = BeautifulSoup(article_view.text, 'html.parser')
    return index_json(bs_article)


if __name__ == "__main__":

    row_list = [["id", "category", "title", "author", "facicle", "year", "start_page", "end_page", "pdf_link"]]
    years = ['2018','2019','2019-2020', '2020-2021']
    #TODO need to review how I am going to iterate all years with the last change in BOE

    for year in years:
        url = f"https://www.boe.es/biblioteca_juridica/anuarios_derecho/anuario.php?id=M_{year}"
        html = get(url)
        bs = BeautifulSoup(html.text, 'html.parser')
        #es = Elasticsearch()
        fascicle = bs.find('h3', {'class': 'fuera'}).string
        if fascicle != "Fascículo1":
            url = f"https://www.boe.es/biblioteca_juridica/anuarios_derecho/anuario.php?id=M_{year}&fasc=1"
            html = get(url)
            bs_fasc_1 = BeautifulSoup(html.text, 'html.parser')
            links_fasc_1 = bs_fasc_1.find('ul', {'class': 'lista-contenido'}).findAll('a', href=re.compile("articulo.php"))
            for link in links_fasc_1:
                metadata_article = sracpping_article(link)
                row_list.append(metadata_article)
                time.sleep(1)


        links = bs.find('ul', {'class': 'lista-contenido'}).findAll('a', href=re.compile("articulo.php"))

        # Access to the article view where is the metadata and the pdf
        for link in links:
            metadata_article = sracpping_article(link)
            row_list.append(metadata_article)
            time.sleep(1)




    with open('racmyp_articles_last.csv', 'w', newline='') as file:
       writer = csv.writer(file)
       writer.writerows(row_list)




