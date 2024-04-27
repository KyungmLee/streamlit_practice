import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.header('연습문제#2')
st.subheader('1. iris 데이터셋을 이용')
st.markdown('1) iris 데이터셋을 데이터프레임으로 표시')
@st.cache_data
def load_iris():
    iris = pd.read_csv('data/iris.csv')
    return iris

iris = load_iris()
st.dataframe(iris)

st.divider()
st.markdown('''2) multiselect를 사용하여 품종(species)을 선택하면,  
 해당 품종의 데이터에 대한 데이터프레임으로 표시''')

spec = st.multiselect('품종을 선택하세요',
                      options = ['setosa', 'versicolor','virginica'],
                      default=['setosa'])

st.dataframe(iris[iris.species.isin(spec)])

st.markdown('''3) 품종을 제외한 4가지 컬럼을 radio 요소를 사용하여 선택하면  
  선택한 컬럼에 대한 히스토그램 그리기(matplotlib)''')

column = st.radio('컬럼을 선택하세요',
                   ['sepal_length', 'sepal_width',
                    'petal_length','petal_width'])

# st.dataframe(iris[columns])
st.markdown(f'히스토그램: {column} ')
fig, ax = plt.subplots()
ax.hist(iris[column])
st.pyplot(fig)

##################################################
st.divider()

st.subheader('2. kor_news 데이터셋을 이용')
st.markdown('''분류의 대분류 기준을 선택하면  
해당 분야의 주요 키워드 20위에 대한 bar chart 표시''')

import numpy as np
from konlpy.tag import Okt
from collections import Counter
from matplotlib import font_manager, rc

# font_name = font_manager.FontProperties(fname='c:/Windows/Fonts/malgun.ttf').get_name()
font_name = 'NanumGothic.ttf'
rc('font', family=font_name)

def preprocess(df):
    df['분류리스트'] = df.분류.str.split('>')
    df['대분류'] = df['분류리스트'].str[0]
    df['중분류'] = df['분류리스트'].str[1]
    df['소분류'] = df['분류리스트'].str[2]
    return df

@st.cache_data
def load_data(file_path):
    df = pd.read_excel(file_path)
    return preprocess(df)

def word_counts_df(df, column_name):
    text = list(df[column_name])
    okt = Okt()
    token_pos = [okt.pos(word) for word in text]

    token_list = []
    for token_tag in token_pos:
        result = []
        for token, tag in token_tag:
            if (len(token) > 1) and (tag not in ['Punctuation',
                                                 'Josa', 'Number',
                                                 'Suffix', 'Foreign']):
                result.append(token)
        token_list.append(result)

    tokens = np.hstack(token_list)
    tokens_cnt = Counter(tokens)
    tokens_df = pd.DataFrame(pd.Series(tokens_cnt), columns=['Freq'])
    sorted_df = tokens_df.sort_values(by='Freq', ascending=False)
    return sorted_df

def select_top_keywords(df, column= '제목', category='경제', top_n=20):
    cate_df = df[df['대분류']==category]
    cnt_df = word_counts_df(cate_df, column)
    st.markdown(f'{category} 분야 Top{top_n} 키워드')
    st.bar_chart(cnt_df.iloc[:top_n])

# file_path = 'data/kor_news_240326.xlsx'
# news = load_data(file_path)
# categories = news.대분류.unique()
# cate = st.selectbox('분야를 선택하세요', categories)
# select_top_keywords(news, '제목', cate, 20)

##############################################
st.divider()
st.subheader('3. 경기도인구데이터에 대하여')
st.markdown('''연도별 인구수에 대한 지도시각화  
   2007년, 2015년, 2017년 연도를 탭으로 제시''')

import json
import folium
from streamlit_folium import st_folium, folium_static
import os
# from utils.map import load_data, load_geo_json, load_excel_data
# from utils.map import draw_map

@st.cache_data
def load_geo_json(file_path):
    with open(file_path, encoding='utf-8') as f:
        geo_gg = json.loads(f.read())
    return geo_gg

@st.cache_data
def load_excel_data(file_path):
    return pd.read_excel(file_path, index_col='구분')

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
                      data=df,
                      columns=[df.index, df[year]],
                      key_on='feature.properties.name').add_to(map)
    # st_folium(map, width=600, height=400)
    folium_static(map, width=600, height=400)
    

file1 = 'data/경기도행정구역경계.json'
file2 = 'data/경기도인구데이터.xlsx'
file3 = 'data/iris.csv'
# df = load_data(file3)

geo_gg = load_geo_json(file1)
df_gg = load_excel_data(file2)
# df_gg.set_index('구분', inplace=True)
st.dataframe(df_gg)

tab1, tab2, tab3 = st.tabs(['2007년','2015년', '2017년'])

with tab1:
    draw_map(2007, geo_gg, df_gg)
    # draw_map(2007)
with tab2:
    draw_map(2015,geo_gg, df_gg)
    # draw_map(2015)
with tab3:
    draw_map(2017, geo_gg, df_gg)
    # draw_map(2017)
