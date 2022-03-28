import os
import streamlit as st
import pandas as pd

def app():

    # Page title
    st.markdown("### Compare tables before and after changes")

    # Create before and after columns
    column_widths = [1, 1]
    c1, c2 = st.columns(column_widths)
    c1.subheader("Before")
    c2.subheader("After")

## Upload before data ##
    data_before = c1.file_uploader("Upload data before changes", type=["csv", "xlsx"])    
    global data1
    if data_before is not None:
        try:
            data1 = pd.read_csv(data_before)
        except Exception as e:
            print(e)
            data1 = pd.read_excel(data_before)

    if c1.button("Load Before Data"):
        if data_before is None:
            c1.markdown("Please select a file to upload first")
        else:
            # Save uploaded CSV as dataframe
            df_before = data1
            c1.markdown("Load Complete")
        

## Upload after data ##
    data_after = c2.file_uploader("Upload data after changes", type=["csv", "xlsx"])    
    global data2
    if data_after is not None:
        try:
            data2 = pd.read_csv(data_after)
        except Exception as e:
            print(e)
            data2 = pd.read_excel(data_after)


    if c2.button("Load After Data"):
        if data_after is None:
            c2.markdown("Please select a file to upload first")
        else:
            # Save uploaded CSV as dataframe
            df_after = data2
            c2.markdown("Load Complete")
        
            # Multiselect for identifying keys
            keys = st.multiselect("Which column(s) are unique keys? (must be the same for both datasets)", df_after.columns)
            if len(keys) > 0:
                st.sidebar.markdown("hello")

        

## Three dividers ##
    st.markdown("---")

    new_rows_expander = st.expander(label="New Rows", expanded=False)

    deleted_rows_expander = st.expander(label="Deleted Rows", expanded=False)

    changed_rows_expander = st.expander(label="Modified Rows", expanded=False)