import streamlit as st
import pandas as pd
import snowflake.connector

st.title('Editable dataframe test app')
st.text('This app just allows you to edit a large dataset 📝 (60 cols x 200k rows) hosted on Snowflake ❄️')

def get_from_snowflake():
    con = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    try:
        cur = con.cursor()
        cur.execute('SELECT * FROM SYNTETIC_DATASET')
        df = cur.fetchall()
    finally:
        con.close()
    return df

def save_to_snowflake():
    pass

df = get_from_snowflake()
edited_df = st.experimental_data_editor(df, key='data_editor')
st.write(st.session_state["data_editor"])

if streamlit.button('Save to Snowflake!'):
    save_to_snowflake()
