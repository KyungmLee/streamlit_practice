import json
import pandas as pd
import os
import streamlit as st
import folium
from streamlit_folium import st_folium, folium_static


@st.cache_data
def load_geo_json(file_path):
    with open(file_path, encoding='utf-8') as f:
        geo_gg = json.loads(f.read())
    return geo_gg

@st.cache_data
def load_excel_data(file_path):
    return pd.read_excel(file_path)

def load_data(file_path):
    fname, ext = os.path.splitext(file_path)
    if ext in ['xlsx', 'xls']:
        return pd.read_excel(file_path)
    elif ext == 'csv':
        return pd.read_csv(file_path, encodings=['utf-8','euc-kr'])

def draw_map(year, geo, df):
    map = folium.Map(location=[37.5666, 126.9782], zoom_start=8)
    folium.GeoJson(geo).add_to(map)
    folium.Choropleth(geo_data=geo,
                      data=df[year],
                      columns=[df.index, df[year]],
                      key_on='feature.properties.name').add_to(map)
    # st_folium(map, width=600, height=400)
    folium_static(map, width=600, height=400)
    
