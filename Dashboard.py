# Create a streamlit map app

import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

# Load data
with open('resources/Top20k_valid.JSON', 'r', encoding='utf-8') as file:
    df = pd.read_json(file)

# drop all columns with NaN values
df.dropna(axis=1, inplace=True)
# rename Latitude and Longitude
df.rename(columns={'Latitude': 'lat', 'Longitude': 'lon'}, inplace=True)

st.title('Kurse - Dashboard')
df

# Drop rows where Bundesland is not BAW or not empty
df = df[(df['Bundesland'] == 'BAW') | (df['Bundesland'] == '')]

# Display number of rows and columns
st.subheader('Number of rows and columns')
st.write(df.shape)

# create an input for the user to select a city
city = st.selectbox('Select a city', df['Anbieterstadt'].unique())

# Create a map with the selected city where the longitude and latitude are not 0
st.subheader('Map')
st.map(df[(df['lat'] != 0) & (df['lon'] != 0)][['lat', 'lon']])

# Create a histogram with the number of courses per city
st.subheader('Number of courses per city')
st.bar_chart(df['Anbieterstadt'].value_counts())

# Create a heatmap with the number of courses per city
st.subheader('Heatmap')
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
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
            radius=100,
            extruded=True,
            pickable=True,
            elevation_scale=4,
            elevation_range=[0, 1000],
        ),
    ],
))

# List number of courses per provider
st.subheader('Number of courses per Veranstaltername')
st.write(df['Veranstaltername'].value_counts())

# List number of courses per city
st.subheader('Number of courses per Kursstadt')
st.write(df['Kursstadt'].value_counts())

# Create 3d map with number of courses per city
st.subheader('3D Map')
st.pydeck_chart(pdk.Deck(
    map_style=None,
    # map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=48.783333,
        longitude=9.183333,
        zoom=7,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=df[['lat', 'lon']],
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=200,
        ),
        pdk.Layer(
            'HexagonLayer',
            data=df[['lat', 'lon']],
            get_position='[lon, lat]',
            radius=4000,
            elevation_scale=4,
            elevation_range=[500, 20000],
            pickable=True,
            extruded=True,
        ),
    ],
))

# Run with streamlit run Dashboard.py
