!
import streamlit as st

# Initialize connection.
conn = st.connection('shopDB', type='sql',
                     url='mysql://streamlit:1234@localhost:3306/shopDB')

# Perform query.
df = conn.query('SELECT * from customer;', ttl=600)

# Print results.
for row in df.itertuples():
    st.write(f"{row.customer_name} has a :{row.phone}:")

st.dataframe(df)

st.write('고객 정보 입력')
with st.form(key='input_form'):
    id = st.number_input('customer_id', min_value=7)
    name = st.text_input('customer_name')
    phone = st.text_input('phone')
    birthday = st.date_input('birthday', value=None)
    submitted = st.form_submit_button('입력')

sql = ''
if submitted:
    sql = r'''insert into customer (customer_id, customer_name, phone, birthday) 
     values (:id, :name, :phone, :birth);'''
    record = {'id':id, 'name':name,
              'phone':phone, 'birth':birthday}
    with conn.session as session:
        session.execute(sql, record)
        session.commit()

    st.write(df)

