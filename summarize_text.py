import spacy
import advertools as adv
from string import punctuation
from collections import Counter
from heapq import nlargest
import pandas as pd


def title_analyzer(title):
    nlp = spacy.load("es_core_news_sm")
    doc = nlp(str(title))
    list_categories = []
    # NOUN Chunks
    for word in doc.noun_chunks:
            #print(entity.text + ' - ' + entity.label_ + ' - ' + str(spacy.explain(entity.label_)))
        list_categories.append(word.text)
        #if (token.tag_ == "NOUN" ) :
            #
            #print(word.text, word.lemma_, word.pos_, word.tag_, word.dep_, word.shape_, word.is_alpha, word.is_stop)

    # TOKENS
    #for token in doc:
    #    if (token.tag_ == "NOUN"):
    #        list_categories.append(token.text)
    #        #print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)
    #TODO Is it the best way to do it ?? prefer only NOUN??
    return list_categories


def process_text(text):
    nlp = spacy.load("es_core_news_sm")
    stop_words = adv.stopwords['spanish']

    keyword = []
    doc = nlp(text)
    print(len(list(doc.sents)))
    pos_tag = ['PROPN', 'ADJ', 'NOUN', 'VERB']

    for token in doc:

        if(token.text in stop_words or token.text in punctuation):
            continue
        if(token.pos_ in pos_tag and len(token.text) > 3):
            keyword.append(token.text)
    return keyword


def read_page(file_name):
    file = open(file_name, "r")
    filedata = file.read()
    return filedata



if __name__ == "__main__":
    input_file = "racmyp_articles_1973.csv"
    df = pd.read_csv(input_file, header=0)

    for index, row in df.iterrows():
        id = row['id']
        title = row['title']
        print("ID: "+ id)
        print(title)
        title_categories = title_analyzer(row['title'])
        print(title_categories)
        doc = read_page("articles_txt/" + str(id) + ".txt")
        text = process_text(doc)
        freq_word = Counter(text)

        max_freq = Counter(text).most_common(1)[0][1]
        for word in freq_word.keys():
            freq_word[word] = (freq_word[word] / max_freq)
        print(freq_word.most_common(5))

        #weighing_sentences()

        nlp = spacy.load("es_core_news_sm")
        doc = nlp(doc)
        sent_strength = {}
        for sent in doc.sents:
            for word in sent:
                if word.text in freq_word.keys():
                    if sent in sent_strength.keys():
                        sent_strength[sent] += freq_word[word.text]
                    else:
                        sent_strength[sent] = freq_word[word.text]

        summarized_sentences = nlargest(3, sent_strength, key=sent_strength.get)
        final_sentences = [w.text for w in summarized_sentences]
        summary = ' '.join(final_sentences)
        text_summary = process_text(summary)
        freq_word_summary = Counter(text_summary)
        
        max_freq_summary = Counter(text_summary).most_common(1)[0][1]
        for word in freq_word_summary.keys():
            freq_word_summary[word] = (freq_word_summary[word] / max_freq_summary)
        print(freq_word_summary.most_common(5))

#TODO check if words appears in both list???