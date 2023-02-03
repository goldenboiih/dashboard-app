import streamlit as st
import streamlit_wordcloud as wordcloud

import pandas as pd
from wordcloud import WordCloud

NUMBER_OF_WORDS_IN_CLOUD = 15


######## calculate provider number of courses ############
with open('resources/Top20k_valid.JSON', 'r', encoding='utf-8') as file:
    df_copy = pd.read_json(file)
provider_names = set(df_copy["Veranstaltername"])
provider_number_of_courses = dict()
for provider in provider_names:
    provider_desc= df_copy.loc[df_copy['Veranstaltername'] == provider]["Kursbeschreibung"]
    if provider == "":
        provider_number_of_courses['no provider given'] = len(provider_desc)
    else:
        provider_number_of_courses[provider] = len(provider_desc)

#########################################################

data_all = pd.read_csv("resources/tf_idf_all_only_nouns.csv").rename(columns={'Unnamed: 0':"words"})
dict_data = data_all.to_dict()



@st.cache
def word_cloud_together():
    word_count= dict()
    for i in range(0,NUMBER_OF_WORDS_IN_CLOUD):
        word_count[dict_data['words'][i]] = dict_data['TF-IDF'][i]*100
    all_words = WordCloud(width=600, height=300).fit_words(word_count)
    return all_words.to_array()

with st.container():
    st.header("Wordcloud for all Courses together:")
    st.image(word_cloud_together())
st.markdown("""---""")
#########################################################
## For each Provider:
@st.cache
def get_all_provider():
    data_provider = pd.read_csv("resources/tf_idf_each_provider.csv").rename(columns={'Unnamed: 0':"words"})
    provider_names = set(data_provider["provider"])
    all_word_clouds = dict()
    for name in provider_names: 
        dict_data  = data_provider.loc[data_provider["provider"] == name].head(10)[["words", "TF-IDF"]]
        dict_data = dict_data.to_dict()
        word_cloud = dict()
        counter = 0
        for id_key in dict_data["words"].keys():
            word_cloud[dict_data['words'][id_key]] = dict_data['TF-IDF'][id_key]
            counter += 1
            if counter == NUMBER_OF_WORDS_IN_CLOUD:
                break
        all_word_clouds[name] = word_cloud
    return all_word_clouds

all_word_clouds = get_all_provider()
with st.container():
    st.header("Wordcloud for a single Course Provider:")
    option = st.selectbox('For which Course would you like to see a Wordcloud?',(all_word_clouds.keys()))


    st.subheader(option)
    st.write("The Provider has "+ str(provider_number_of_courses[option])+" courses.")
    wc = WordCloud(width=600, height=300).fit_words(all_word_clouds[option])
    st.image(wc.to_array())


