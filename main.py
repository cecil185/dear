import streamlit as st
import pandas as pd
import plotly.express as px

from utils import create_snowflake_connector, DbtProfiles


## Delete

## GET DATA


def load_data():
    file_name = "data/podcasts.csv"
    title = file_name.split("/")[-1]
    return title, pd.read_csv(file_name)


app_title, df = load_data()

## DO WORK

list_nulls = []
list_colNames = []
list_type = []
for col in df.columns:
    list_nulls.append(round(sum(df[col].isna()) / df.shape[0] * 100, 3))
    list_colNames.append(col)
    if df[col].dtype == "int64" or df[col].dtype == "float64":
        list_type.append("Num")
    elif df[col].dtype == "object":
        list_type.append("Cat")
    else:
        list_type.append(None)
        print("Unknown data type for ", df[col].dtype)

if len(list_colNames) != len(list_nulls) or len(list_colNames) != len(list_type):
    print("ERROR, length of column names, null, or type lists do not match")
else:
    df_null = pd.DataFrame(
        {"Percent_Null": list_nulls, "Data_Type": list_type}, index=list_colNames
    )

df_null = df_null.reset_index().rename(columns={"index": "TITLE"})

# create donut chart
fig = px.pie(df_null, values="Percent_Null", names="TITLE")


#################################################
# State Vars
#################################################

if "tables" not in st.session_state:
    st.session_state.tables = []

if "table_data" not in st.session_state:
    st.session_state.table_data = None


#################################################
# Helper Functions
#################################################


def create_db_connection():
    if st.session_state.selected_profile is None:
        return None

    profile_data = DbtProfiles().get(st.session_state.selected_profile)

    if profile_data is None:
        return None

    return create_snowflake_connector(profile_data)


def fetch_table_names(profilss=None):
    conn = create_db_connection()
    cur = conn.cursor()

    cur.execute(
        "select * from INFORMATION_SCHEMA.TABLES where table_schema != 'INFORMATION_SCHEMA'"
    )
    results = cur.fetchall()
    st.write(results)
    results = [".".join(row[:3]) for row in results]

    st.write(results)
    st.session_state.tables = results


def process_table():
    # Create Conn
    conn = create_db_connection()
    if conn is None:
        return
    cur = conn.cursor()
    cur.execute(f"select * from {st.session_state.selected_table} limit 100")
    df = cur.fetch_pandas_all()
    st.session_state.table_data = df
    # Get Table INFO


#################################################
# Streamlit UI
#################################################

with st.sidebar.form("profile_select"):

    st.selectbox(
        "Select a DBT Profile",
        options=[None] + DbtProfiles().list(),
        key="selected_profile",
    )

    st.form_submit_button("Set Profile", on_click=fetch_table_names)

if len(st.session_state.tables) > 0:
    with st.sidebar.form("db_fetch"):
        st.selectbox("Select Table", st.session_state.tables, key="selected_table")
        st.form_submit_button("Analyze Table ", on_click=process_table)


## Display
st.title(f"DEAR: {app_title}")
st.write(st.session_state.table_data)
# display donut chart
st.plotly_chart(fig)
