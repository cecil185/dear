import os
import streamlit as st
import pandas as pd
from functions.dataset_ops import getElementsNotSharedInLists

def app():

    # Page title
    st.markdown("### Compare tables before and after changes")

    # Create before and after columns
    column_widths = [1, 1]
    c1, c2 = st.columns(column_widths)
    c1.subheader("Before")
    c2.subheader("After")

    # If flags are already initialized, don't do anything
    if 'f1' not in st.session_state:
        st.session_state.f1 = False
    if 'f2' not in st.session_state:
        st.session_state.f2 = False
    if 'df_before' not in st.session_state:
        st.session_state.df_before = None
    if 'df_after' not in st.session_state:
        st.session_state.df_after = None

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
            st.session_state.df_before = data1
            c1.markdown("Load Complete")
            st.session_state.f1=True
        

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
            st.session_state.df_after = data2
            c2.markdown("Load Complete")
            st.session_state.f2=True


    if st.session_state.f1 and st.session_state.f2:
        # Multiselect for identifying keys
        keys = st.multiselect("Which column(s) are unique keys? (must be the same for both datasets)", st.session_state.df_after.columns)
        if len(keys) > 0:
            #initialize key columns
            st.session_state.df_before['key']=''
            st.session_state.df_after['key']=''
            
            #create new column key which combines all key columns
            for k in keys:
                st.session_state.df_before['key']+=st.session_state.df_before[k].astype(str)
                st.session_state.df_after['key']+=st.session_state.df_after[k].astype(str)
            
            #if unique combo is not unique there will be a problem

            #gets new and deleted rows
            list1=st.session_state.df_before['key']
            list2=st.session_state.df_after['key']
            new_rows_list, deleted_rows_list = getElementsNotSharedInLists(list1, list2)

            st.write(new_rows_list)
            st.write(deleted_rows_list)
            
            #gets new and deleted columns
            list1=st.session_state.df_before.columns
            list2=st.session_state.df_after.columns
            new_cols_list, deleted_cols_list = getElementsNotSharedInLists(list1, list2)

            st.write(new_cols_list)
            st.write(deleted_cols_list)

        ## Three dividers ##
        st.markdown("---")

        new_rows_expander = st.expander(label="New Rows", expanded=False)
        #with new_rows_expander:
            
        deleted_rows_expander = st.expander(label="Deleted Rows", expanded=False)
        #with deleted_rows_expander:
            
        changed_rows_expander = st.expander(label="Modified Rows", expanded=False)

