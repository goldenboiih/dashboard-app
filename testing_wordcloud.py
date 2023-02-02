import pandas as pd
import re
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
import json

nlp = spacy.load("de_core_news_sm")
with open('resources/Top20k_valid.JSON', 'r', encoding='utf-8') as file:
    df = pd.read_json(file)





def clean_data(data:list, allowed_word_types = []):
    """
    # [ "NOUN", "PROPN"]
    """
    for sentence in data:
        sentence, n = re.subn('[:]', ' ', sentence)
        sentence, n = re.subn('[.!?]', ' . ', sentence)
        if allowed_word_types != []:
            sentence = " ".join([w .text for w in nlp(sentence) if w.pos_ in allowed_word_types])
    return data


def calculate_tf_idf_score(descriptions: list, allowed_word_types = []):
    """
    Calculates the TF-IDF Score for a list of sentences, after cleaning the data
    """
    descriptions = clean_data(descriptions, allowed_word_types)
    tfIdfVectorizer=TfidfVectorizer(use_idf=True)
    tfIdf = tfIdfVectorizer.fit_transform(descriptions)
    df = pd.DataFrame(tfIdf[0].T.todense(), index=tfIdfVectorizer.get_feature_names(), columns=["TF-IDF"])
    df = df.sort_values('TF-IDF', ascending=False)
    #print (df.head(25))
    return df


descriptions_all = [i for i in list(df["Kursbeschreibung"]) if i != ""]
tf_idf_all = calculate_tf_idf_score(descriptions_all, ["NOUN", "PROPN"])
tf_idf_all.to_csv('resources/tf_idf_all.csv')
