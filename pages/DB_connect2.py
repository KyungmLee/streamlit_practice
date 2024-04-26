import streamlit as st
import mysql.connector
import pandas as pd

conn = mysql.connector.connect(
    host = 'localhost',
    database = 'shopDB',
    user = 'streamlit',
    password ='1234'
)

if conn.is_connected():
    db_info = conn.get_server_info()
    st.write('server_version: ', db_info)

cursor = conn.cursor()
cursor.execute('select database();')

record = cursor.fetchone()
st.write('connected to DB : ', record)

cursor.execute('select * from customer;')
records = cursor.fetchall()
df = pd.DataFrame(records,
                  columns=['id','name','phone','birthday'])

st.write(df)

with st.form(key='input_form'):
    id = st.number_input('customer_id', min_value=7)
    name = st.text_input('customer_name')
    phone = st.text_input('phone')
    birthday = st.date_input('birthday', value=None)
    submitted = st.form_submit_button('입력')

sql = ''
if submitted:
    sql = ('insert into customer (customer_id, customer_name, phone, birthday) ' \
        + 'values (' + str(id) + ', \"' + name + '\", \"' \
           + phone + '\", \"' + str(birthday) +'\");')
    cursor.execute(sql)
    conn.commit()
    st.write('**데이터 삽입 결과**')
    cursor.execute('select * from customer;')
    records = cursor.fetchall()
    df = pd.DataFrame(records,
                      columns=['id','name','phone','birthday'])

    st.write(df)
