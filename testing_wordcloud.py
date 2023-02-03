import pandas as pd
import re
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer

# Barchart(s): Andy
# Heatmap: Kenny
# Wordcloud: Katrin
# General Overview: #Anbieter #Kurse #Städte
# Kurse nach Monat


nlp = spacy.load("de_core_news_sm")
with open('resources/Top20k_valid.JSON', 'r', encoding='utf-8') as file:
    df = pd.read_json(file)

def clean_data(data:list, allowed_word_types = []):
    """
    # [ "NOUN", "PROPN"]
    """
    new_data = []
    for sentence in data:
        sentence, n = re.subn('[:]', ' ', sentence)
        sentence, n = re.subn('[.!?]', ' . ', sentence)
        if allowed_word_types != []:
            sentence = " ".join([w.text for w in nlp(sentence) if w.pos_ in allowed_word_types])
        new_data.append(sentence)
            
    return new_data


def calculate_tf_idf_score(descriptions: list, allowed_word_types = []):
    """
    Calculates the TF-IDF Score for a list of sentences, after cleaning the data
    """
    descriptions = clean_data(descriptions, allowed_word_types)
    try:
        tfIdfVectorizer=TfidfVectorizer(use_idf=True, min_df=1)
    
        tfIdf = tfIdfVectorizer.fit_transform(descriptions)
        df = pd.DataFrame(tfIdf[0].T.todense(), index=tfIdfVectorizer.get_feature_names(), columns=["TF-IDF"])
        df = df.sort_values('TF-IDF', ascending=False)
    #print (df.head(25))
        return df
    except:
        print(descriptions)
        for i in descriptions:
            
            print(TfidfVectorizer().build_analyzer()(i))
        return None


## Get all data 
def get_tf_idf_all_together():
    """
    Calculates the TF-IDF score for all "Kursbeschreibungen" in the dataset
    """
    descriptions_all = [i for i in list(df["Kursbeschreibung"]) if i != ""][1:10]
    tf_idf_all = calculate_tf_idf_score(descriptions_all, ["NOUN", "PROPN"])
    tf_idf_all.to_csv('resources/tf_idf_all_only_nouns.csv')

  
def load_all_data():   
    """
    Testfunction for loading the data and shaping it for the wordcloud
    """ 
    data = pd.read_csv("resources/tf_idf_all.csv").rename(columns={'Unnamed: 0':"words"})
    dict_data = data.to_dict()
    print(dict_data.keys())
    word_cloud = list()
    for i in range(0,15):
        word_cloud.append({"text": dict_data['words'][i], "value": dict_data['TF-IDF'][i] })
    print(word_cloud)

####

def get_descriptions_for_provider():
    """ 
    Obtains all non-empty "Kursbeschreibungen" from the dataset for each provider
    """
    provider_names = set(df["Veranstaltername"])
    provider_descriptions = dict()
    tmp_df = df[df['Kursbeschreibung'] != ""]
    for provider in provider_names:
        provider_desc= tmp_df.loc[tmp_df['Veranstaltername'] == provider]["Kursbeschreibung"]
        
        if len(provider_desc) > 1:
            if provider == "":
                provider_descriptions["no provider given"] = provider_desc
            else: 
                provider_descriptions[provider] = provider_desc
        else:
            print(provider)

    return provider_descriptions


def get_all_provider():
    """ 
    Calculates the TF-IDF score for all "kursbeschreibungen" belonging 
    to each "Veranstalter" and writes it into a csv file
    """
    all_provider_descriptions = get_descriptions_for_provider()
    frames = []
    for prov in all_provider_descriptions.keys():
        tmp_tf_idf_score = calculate_tf_idf_score(all_provider_descriptions[prov],  [])
        tmp_tf_idf_score["provider"] = str(prov)
        frames.append(tmp_tf_idf_score)
    result = pd.concat(frames)
    result.to_csv('resources/tf_idf_each_provider_all_wordtypes.csv')

#get_tf_idf_all_together()
get_all_provider()



"""
data_provider = pd.read_csv("resources/tf_idf_each_provider.csv").rename(columns={'Unnamed: 0':"words"})
provider_names = set(data_provider["provider"])
all_word_clouds = dict()
for name in provider_names:
    
    dict_data  = data_provider.loc[data_provider["provider"] == name].head(10)[["words", "TF-IDF"]]
    dict_data = dict_data.to_dict()
    word_cloud = list()
    counter = 0
    for id_key in dict_data["words"].keys():
        word_cloud.append({"text": dict_data['words'][id_key],
                           "value": dict_data['TF-IDF'][id_key] })
        counter += 1
        if counter == 15:
            break
    all_word_clouds[name] = word_cloud

print(all_word_clouds)
"""

