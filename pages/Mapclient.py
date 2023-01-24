import folium
from streamlit_folium import st_folium, folium_static
import streamlit as st
from Dashboard import df

df_copy = df.copy()
# Check rows where lat and lon are unique
st.write(df_copy.shape)
df_copy.drop_duplicates(subset=['lat', 'lon'], inplace=True)
st.write(df_copy.shape)

# Make an empty map
map = folium.Map(location=[48.783333, 9.183333], tiles="OpenStreetMap", zoom_start=9)

# I can add marker one by one on the map
for i in range(0, 294):
    folium.Marker([df.iloc[i]['lat'], df.iloc[i]['lon']],
                  popup=df.iloc[i]['Anbieterstadt']).add_to(map)

st_map = folium_static(map)
