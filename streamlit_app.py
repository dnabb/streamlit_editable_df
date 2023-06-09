import streamlit as st
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

st.set_page_config(layout="wide")

st.title('Editable dataframe test app')
st.text('This app just allows you to edit a large dataset 📝 (60 cols x 200k rows) hosted on Snowflake ❄️')

def get_from_snowflake():
    con = snowflake.connector.connect(**st.secrets["snowflake"])
    try:
        cur = con.cursor()
        cur.execute('SELECT * FROM SYNTETIC_DATASET_T')
        df = cur.fetch_pandas_all().set_index('PK')

    finally:
        con.close()
    return df

# Very inefficient "full reload" logic
def save_to_snowflake(df):
    con = snowflake.connector.connect(**st.secrets["snowflake"])
    try:
        cur = con.cursor()
        cur.execute('CREATE TEMPORARY TABLE SYNTETIC_DATASET_EDITED LIKE SYNTETIC_DATASET_T')
        success, nchunks, nrows, output = write_pandas(con, df, 'SYNTETIC_DATASET_EDITED')
        if success:
            cur.execute('CREATE OR REPLACE TRANSIENT TABLE SYNTETIC_DATASET_T CLONE SYNTETIC_DATASET_EDITED')
    finally:
        con.close()
    return success

df = get_from_snowflake()

edited_df = st.experimental_data_editor(df, key='data_editor')
# st.write(st.session_state["data_editor"])

if st.button('Save to Snowflake!'):
    save_to_snowflake(edited_df)
    df = edited_df
