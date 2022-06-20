
from elasticsearch import Elasticsearch
from csv import reader


def categories(text):
    list_categories = []
    if len(text.split(" ")) == 3:
        list_categories = text.split(" y ")
    list_categories.append(text)

    return list_categories



if __name__ == "__main__":

    es = Elasticsearch()

    with open('racmyp_articles_1973.csv', 'r') as articles:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(articles)
        header = next(csv_reader)
        if header != None:
            # Iterate over each row in the csv using reader object
            for row in csv_reader:
                # row variable is a list that represents a row in csv
                print(row)
                article_json = {
                    'categories': categories(row[1]),
                    'title_categories':  [],
                    'title':      row[2],
                    'author':     row[3],
                    'facicle':    row[4],
                    'year':       row[5],
                    'start_page': row[6],
                    'end_page':   row[7],
                    'pdf_link':   row[8]
                }
                es.index(index="articles", id=row[0], document=article_json)