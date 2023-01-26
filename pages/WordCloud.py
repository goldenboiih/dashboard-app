import streamlit as st
import streamlit_wordcloud as wordcloud
from Dashboard import df

df_copy = df.copy()

# get words from beschreibung

# extract all nouns
# count them
"""
    ## Testing WordCloud
    descriptions = [i for i in list(df["Kursbeschreibung"]) if i != ""]
    joined_descriptions = " ".join(descriptions)
    doc = nlp(joined_descriptions)
    nouns =[w for w in doc]# if w.pos_ in[ "NOUN", "PROPN"]]

    word_counts = list()
    for n in nouns:
        word_counts.append({"text":n, "value": nouns.count(n)})
        if nouns.count(n) > 1:
            print(n, nouns.count(n))
"""

words = [
    dict(text="Robinhood", value=16000, country="US", industry="Cryptocurrency"),
    dict(text="Personio", value=8500,  country="DE", industry="Human Resources"),
    dict(text="Boohoo", value=6700, country="UK", industry="Beauty"),
    dict(text="Deliveroo", value=13400, country="UK", industry="Delivery"),
    dict(text="SumUp", value=8300,  country="UK", industry="Credit Cards"),
    dict(text="CureVac", value=12400, country="DE", industry="BioPharma"),
    dict(text="Deezer", value=10300,country="FR", industry="Music Streaming"),
    dict(text="Eurazeo", value=31, country="FR", industry="Asset Management"),
    dict(text="Drift", value=6000,  country="US", industry="Marketing Automation"),
    dict(text="Twitch", value=4500,  country="US", industry="Social Media"),
    dict(text="Plaid", value=5600,  country="US", industry="FinTech"),
]
return_obj = wordcloud.visualize(words, tooltip_data_fields={
    'text':'Company', 'value':'Mentions', 'country':'Country of Origin', 'industry':'Industry'
    }, per_word_coloring=False)
