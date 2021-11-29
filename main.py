import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

## Delete
import seaborn as sns

## GET DATA


def load_data():
    file_name = "data/podcasts.csv"
    title = file_name.split("/")[-1]
    return title, pd.read_csv(file_name)


app_title, df = load_data()
print(df.columns)
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
print(df_null)

df_null = df_null.reset_index().rename(columns={"index": "TITLE"})

# create donut chart
fig = px.pie(df_null, values="Percent_Null", names="TITLE")


## Display
st.title(f"DEAR: {app_title}")

# display donut chart
st.plotly_chart(fig)
