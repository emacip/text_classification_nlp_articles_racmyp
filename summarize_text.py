import spacy
import advertools as adv
from string import punctuation
from collections import Counter
from heapq import nlargest
import pandas as pd
from elasticsearch import Elasticsearch


def process_text(text):
    nlp = spacy.load("es_core_news_sm")
    stop_words = adv.stopwords['spanish']

    keyword = []
    doc = nlp(text)
    # print(len(list(doc.sents)))
    pos_tag = ['PROPN', 'ADJ', 'NOUN', 'VERB']

    for token in doc:

        if (token.text in stop_words or token.text in punctuation):
            continue
        if (token.pos_ in pos_tag and len(token.text) > 3):
            keyword.append(token.text)
    return keyword


def read_page(file_name):
    file = open(file_name, "r")
    filedata = file.read()
    return filedata


def most_freq_words(text):
    freq_word = Counter(text)
    max_freq = Counter(text).most_common(1)[0][1]
    for word in freq_word.keys():
        freq_word[word] = (freq_word[word] / max_freq)
    return freq_word


def summarize(document, per):
    nlp = spacy.load("es_core_news_sm")
    stop_words = adv.stopwords['spanish']
    doc = nlp(document)
    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in list(stop_words):
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    max_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / max_frequency
    sentence_tokens = [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]
    select_length = int(len(sentence_tokens) * per)
    summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)
    final_summary = [word.text for word in summary]
    summary = ''.join(final_summary)
    return summary


def remove_stopwords(text, nlp):
    text = text.lower().title()
    doc = nlp(str(text))
    tokens = [token.text for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(tokens)






if __name__ == "__main__":
    input_file = "racmyp_articles_all.csv"
    df = pd.read_csv(input_file, header=0)
    es = Elasticsearch()
    nlp = spacy.load("es_core_news_sm")

    for index, row in df.iterrows():
        id = row['id']

        doc = read_page("articles_txt/" + str(id) + ".txt")
        # Process full document
        text = process_text(doc)
        summary = summarize(doc, 0.3)

        # Process summary document
        text_summary = process_text(summary)
        if text_summary != []:
            # most repeated words in the summary
            most_repeated_words = most_freq_words(text_summary).most_common(5)
            summary_tokens = []

            for word in most_repeated_words:
                new_word = remove_stopwords(word[0], nlp)
                if new_word != "" and new_word not in summary_tokens:
                    summary_tokens.append(new_word)


            body_json = {
               'doc': { 'summarize_categories': summary_tokens }
            }
            es.update(index='articles', id=id, body=body_json)

        print(".")