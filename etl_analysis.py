import numpy as np
import pandas as pd
import csv
import spacy
from ast import literal_eval
from elasticsearch import Elasticsearch



def title_analyzer(title):
    nlp = spacy.load("es_core_news_sm")
    doc = nlp(str(title))


    print(title)
    # Extract the noun phrases from the document
    noun_phrases = []
    for chunk in doc.noun_chunks:
        if len(chunk) >= 1:
            noun_phrases.append(chunk)

    # Extract the individual nouns from the noun phrases
    nouns = []
    for phrase in noun_phrases:
        for token in phrase:
            if len(token) > 2 and (token.pos_ == "NOUN" or token.pos_ == "PROPN"):
                new_phrase = remove_stopwords(phrase.text, nlp)
                if new_phrase != "":
                    nouns.append(new_phrase)
                    break

    # Print the result
    print(nouns)
    return nouns


def remove_stopwords(text, nlp):
    if text.isupper():
        text = text.lower()
    doc = nlp(str(text))

    tokens = [token.text for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(tokens)






if __name__ == "__main__":
    #corpus_path = r"articles_pdf" #TODO ???? can we deleted?
    input_file = "racmyp_articles_all.csv"
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



