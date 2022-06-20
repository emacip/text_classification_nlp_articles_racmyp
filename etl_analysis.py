import numpy as np
import pandas as pd
import csv
import spacy
from ast import literal_eval
from elasticsearch import Elasticsearch



def title_analyzer(title):
    nlp = spacy.load("es_core_news_sm")
    doc = nlp(str(title))
    list_categories = []
    # NOUN Chunks
    print("NOUN Chunks")
    for word in doc.noun_chunks:
            #print(entity.text + ' - ' + entity.label_ + ' - ' + str(spacy.explain(entity.label_)))
        list_categories.append(word.text)
        #if (token.tag_ == "NOUN" ) :
        print(word.text, word.root.text, word.root.dep_,word.root.head.text)

    # TOKENS
    print("TOKENS")

    for token in doc:

        if (token.tag_ == "NOUN"):
            #list_categories.append(token.text)
            print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)
    #TODO Is it the best way to do it ?? prefer only NOUN??
    return list_categories



#TODO check update ES index


if __name__ == "__main__":
    corpus_path = r"articles_pdf"
    input_file = "racmyp_articles_1973.csv"
    es = Elasticsearch()
    # comma delimited is the default
    #df = pd.read_csv(input_file, header=0, converters={'category': literal_eval})
    df = pd.read_csv(input_file, header=0)
    #list_categories = df.category.explode().unique()
    for index, row in df.iterrows():
        title_categories = title_analyzer(row['title'])

        body_json = {
            'doc': {'title_categories': title_categories}
        }

        es.update(index='articles', id=row['id'], body=body_json)



    # put the original column names in a python list
    #original_headers = list(df.columns.values)



