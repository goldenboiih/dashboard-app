# Create a streamlit map app
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
import io
from PIL import Image

# Load data
with open('resources/Top20k_valid.JSON', 'r', encoding='utf-8') as file:
    df = pd.read_json(file)

# drop all columns with NaN values
df.dropna(axis=1, inplace=True)
# rename Latitude and Longitude
df.rename(columns={'Latitude': 'lat', 'Longitude': 'lon'}, inplace=True)

st.title('Kurse - Dashboard')

# Drop rows where Bundesland is not BAW or not empty
# df = df[(df['Bundesland'] == 'BAW') | (df['Bundesland'] == '')]

# define tabs
tab1, tab2, tab3, tab4, tab5, tab7 = st.tabs(['Start', 'City Map', 'Courses per city', 'Heatmap',
                                              'Courses per provider', 'Courses per Month'])

with tab1:
    # provide overview
    st.write('Example data entries')
    st.write(df.head(5))
    st.write(f'Total number of courses: {df.shape[0]}')
    st.write(f'Number of features per course: {df.shape[1]}')

with tab2:
    # create an input for the user to select a city
    city = st.selectbox('Select a city', df['Anbieterstadt'].unique())

    # Create a map with the selected city where the longitude and latitude are not 0
    st.subheader('Map')
    st.map(df[(df['Anbieterstadt'] == city) & (df['lat'] != 0) & (df['lon'] != 0)][['lat', 'lon']])

with tab3:
    # Create a histogram with the number of courses per city
    st.subheader('Number of courses per city')
    st.bar_chart(df['Anbieterstadt'].value_counts())

    # List number of courses per city
    st.subheader('Top 10 Number of courses per Kursstadt')
    course_count = df['Anbieterstadt'].value_counts(normalize=True).head(10)
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.pie(course_count, labels=course_count.index, autopct='%1.1f%%')
    ax.axis('equal')
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')
    im = Image.open(img_buf)
    st.image(im)

with tab4:
    # Create a heatmap with the number of courses per city
    st.subheader('Heatmap')
    st.pydeck_chart(pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=48.783333,
            longitude=9.183333,
            zoom=7,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                'HeatmapLayer',
                data=df[['lat', 'lon']],
                get_position='[lon, lat]',
                radius=5000,
                extruded=True,
                pickable=True,
                elevation_scale=4,
                elevation_range=[0, 1000],
            ),
        ],
    ))

with tab5:
    # List number of courses per provider
    st.subheader('Top 10 Number of courses per Veranstaltername')
    course_count = df['Veranstaltername'].value_counts(normalize=True).head(10)
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.pie(course_count, labels=course_count.index, autopct='%1.1f%%')
    ax.axis('equal')
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')
    im = Image.open(img_buf)
    st.image(im)

with tab7:
    # No. of courses per month
    df['Monat'] = pd.to_datetime(df['Kursbeginn']).dt.month
    # df['Monat'] = df['Monat'].astype(int)

    months = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli',
              'August', 'September', 'Oktober', 'November', 'Dezember']

    courses_per_month = df['Monat'].value_counts().sort_index()
    courses_per_month.index = courses_per_month.index.map(lambda x: months[int(x-1)])
    st.write(courses_per_month)
    st.subheader('Number of courses per month')
    # Not easy to retain the order with streamlit
    # https://github.com/streamlit/streamlit/issues/385
    st.bar_chart(courses_per_month)

# Run with streamlit run Dashboard.py
