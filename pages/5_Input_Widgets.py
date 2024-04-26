import streamlit as st

st.title('Input Widgets!')
st.header('1. Button elements' )
st.subheader('Button')
st.button('초기화', type='primary')
if st.button('안녕'):
    st.write('반가워 :simile:')
else:
    st.write('잘가! :raising_hand:')

st.subheader('Link Button')
st.link_button('google', 'https://www.google.com')

st.subheader('Page Link', divider=True)
st.page_link('app.py', label='Home', icon='🏠')
st.page_link('pages/1_Text_elements.py',
             label='Text elements')
st.page_link('pages/2_Data_elements.py',
             label='Data elements')
st.page_link('pages/연습문제1.py', label='Exercise',
             disabled=True)
st.page_link('https://docs.streamlit.io/develop/api-reference',
             label='Streamlit Docs', icon='🌎')

st.subheader('Form Submit_Button', divider=True)

with st.form(key='form1'):
    id = st.text_input('Id')
    pw = st.text_input('Password', type='password')
    submitted = st.form_submit_button('로그인')
if submitted:
    st.write('id :', id, 'password :', pw)

form = st.form(key='form2')
title = form.text_input('제목')
contents = form.text_area(('질문입력'))
submit = form.form_submit_button('작성')
if submit:
    st.write('제목 :',title)


st.divider()
st.header('2. Selection elements')
st.subheader('Checkbox')

agree = st.checkbox('찬성', value=True, label_visibility='visible')
if agree:
    st.write('Good!')

st.subheader('Toggle')
on = st.toggle('선택')
if on:
    st.write('on')

st.subheader('Radio')
fruit = st.radio(
    label = '좋아하는 과일은?',
    options = ['바나나','딸기','메론','사과','배'],
    captions=['웃어요','달콤해요','시원해요',
              '상큼해요','즙이많아요'
    ],
    horizontal=True,
    index=1
)
if fruit=='바나나':
    st.write('바나나를 선택했군요')
else:
    st.write('바나나가 아니네~~')

st.subheader('Selectbox')
fruit = st.selectbox('과일을 선택하세요',
             ['바나나','딸기','사과','메론'],
                     index=None,
                     placeholder='과일을 선택해요!',
                     label_visibility='collapsed')
st.write(f'당신이 선택한 과일은 {fruit}')
st.divider()

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

col1, col2 = st.columns(2)

with col1:
    st.checkbox("Disable selectbox widget", key="disabled")
    st.radio(
        "Set selectbox label visibility 👉",
        key="visibility",
        options=["visible", "hidden", "collapsed"],
    )

with col2:
    option = st.selectbox(
        "How would you like to be contacted?",
        ("Email", "Home phone", "Mobile phone"),
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
    )

st.divider()

st.subheader('Multiselect')
colors = st.multiselect('당신이 좋아하는 색상은?',
                        options=['red','green','blue','yellow','pink'],
                        default=['green', 'blue']
                        )
st.write('선택한 색상은 ', colors)

st.subheader('Selectslider')
color = st.select_slider('당신이 좋아하는 색상은',
                 options=['red','green','blue','yellow','pink',
                          'violet','indigo','orange'])
st.write('당신이 좋아하는 색상은', color)

color = st.select_slider('당신이 좋아하는 색상은',
                 options=['red','green','blue','yellow','pink',
                          'violet','indigo','orange'],
                value='blue')
color_st, color_end = st.select_slider('당신이 좋아하는 색상은',
                 options=['red','green','blue','yellow','pink',
                          'violet','indigo','orange'],
                value=('blue', 'pink'))
st.write('당신이 좋아하는 색상은', color_st, color_end)


st.subheader('color picker')
color = st.color_picker('Pick A Color', '#00f900')
st.write('The current color is', color)

st.header('3. Numeric Input elements')
st.subheader('Number input')
num = st.number_input('숫자입력')
st.write(num)

num = st.number_input('숫자입력', value=None,
                      placeholder='숫자를 입력하세요')
st.write(f'현재숫자: {num}')

num = st.number_input('숫자입력', min_value=-10.0,
                      max_value=10.0, step=0.05,
                      format='%.2f'
                      )
st.write(f'현재숫자: {num:.2f}')

st.subheader('slider')
age = st.slider('나이', min_value=0, max_value=100, value=20, step=2)
st.write(age)

scores = st.slider('점수대',
                   min_value=0.0, max_value=100.0, value=(25.0, 50.0))
st.write(scores)

st.header('4. Text input elements')
st.subheader('Text input')
id = st.text_input('아이디', value='id')
pw = st.text_input('비밀번호', type='password')
st.write(f'아이디: {id}  비밀번호: {pw}')

st.subheader('Text area')
text = st.text_area('질문을 입력하세요')
st.write(text)
st.write(f'총문자길이는 {len(text)}')

st.header('5. Data&Time input elements')
st.subheader('Date input')

from datetime import datetime, date, time, timedelta


date = st.date_input('일자 선택', value=date(2024, 3,1),
                     min_value=date(2023,1,1),
                     max_value=date(2024,12,31),
                     format='YYYY.MM.DD')
st.write(date)

st.subheader('Time input')
time = st.time_input('시간 입력',
                     value=time(8,00),
                     step=timedelta(minutes=10)
                     )
st.write(time)


