# 뉴스 데이터 kor_news_20240326.xlsx를 이용
#
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from matplotlib import font_manager, rc
from konlpy.tag import Okt, Kkma
from collections import Counter
import streamlit as st


# font_name = font_manager.FontProperties(fname='c:/Windows/Fonts/malgun.ttf').get_name()
font_name = 'NanumGothic.ttf'
rc('font', family=font_name)

st.header('연습문제')
st.subheader('1. 뉴스 데이터를 dataframe으로 표시하기')

file_path = 'data/kor_news_240326.xlsx'

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

news = load_data(file_path)
# news = pd.read_excel('data/kor_news_240326.xlsx')
st.dataframe(news)

st.subheader('2. URL column configuration')
st.data_editor(news,
               column_config={
                   'URL': st.column_config.LinkColumn(
                       help = '기사 링크',
                       max_chars = 200
                   )
               })

st.subheader('3. 대분류 컬럼에 대한 빈도 bar chart')

df = pd.DataFrame(news.대분류.value_counts())
st.bar_chart(df)

'''
st.subheader('''4. 제목 컬럼 주요 키워드 20위''')

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

df_econo = news[news['대분류']=='경제']
df_econo_cnt = word_counts_df(df_econo, '제목')
st.markdown('경제 분야 Top20 키워드')
st.bar_chart(df_econo_cnt.iloc[:20])

df_society = news[news['대분류']=='사회']
df_society_cnt = word_counts_df(df_society, '제목')
st.markdown('정치 분야 Top20 키워드')
st.bar_chart(df_society_cnt.iloc[:20])

'''
