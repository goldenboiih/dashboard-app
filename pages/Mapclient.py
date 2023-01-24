import folium
from streamlit_folium import st_folium, folium_static
import streamlit as st
from Dashboard import df

df_copy = df.copy()
# Check rows where lat and lon are unique
st.write(df_copy.shape)
df_copy.drop_duplicates(subset=['lat', 'lon'], inplace=True)
st.write(df_copy.shape)

# Drop rows where

# Make an empty map
map = folium.Map(location=[48.783333, 9.183333], tiles="OpenStreetMap", zoom_start=9)

# Add marker one by one on the map
# List of marker icons: https://fontawesome.com/icons?d=gallery
for i in range(0, len(df_copy)):
    folium.Marker(
        [df.iloc[i]['lat'],
         df.iloc[i]['lon']],
        popup=df.iloc[i]['Anbieterstadt'],
        icon=folium.Icon(color="green")).add_to(map)

st_map = folium_static(map)

df_copy
