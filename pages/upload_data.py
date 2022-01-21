import os
import pandas as pd
import streamlit as st


def app():
    # # Check if data file or file name exists from last run of this app and if so,delete it.
    # if os.path.exists("data/main_data.csv"):
    #     os.remove("data/main_data.csv")
    # if os.path.exists("data/uploaded_file_name.txt"):
    #     os.remove("data/uploaded_file_name.txt")

    st.markdown("## Data Upload")

    # Upload the dataset and save as csv
    st.markdown("### Upload a csv file for analysis.")
    st.write("\n")

    # Code to read a single file
    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])
    global data

    if uploaded_file is not None:
        try:
            data = pd.read_csv(uploaded_file)
        except Exception as e:
            print(e)
            data = pd.read_excel(uploaded_file)

        # Create text file with name of uploaded file
        text_file = open("data/uploaded_file_name.txt", "w")
        text_file.write(uploaded_file.name)
        text_file.close()

    if st.button("Load Data"):
        # Display uploaded CSV
        st.dataframe(data)

        # Save uploaded CSV as file main_data.csv
        data.to_csv("data/main_data.csv", index=False)
