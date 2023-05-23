import numpy as np
import os
import pandas as pd
import streamlit as st

from functions.dataset_ops import getElementsNotSharedInLists
from functions.utils import initialize_session_state, upload_data
from functions.snowflake_connection import create_snowflake_session, get_snowflake_model, get_connection_details, write_connection_details

def app():

    # Page title
    st.markdown("### Compare data models before and after changes")

    # Call function to create new or get existing Snowpark session to connect to Snowflake
    session = create_snowflake_session()

    # initialize_session_state('snowflake_database_1', get_connection_details(session, 'current_database()'))
    # initialize_session_state('snowflake_database_2', get_connection_details(session, 'current_database()'))
    # initialize_session_state('snowflake_schema_1', get_connection_details(session, 'current_schema()'))
    # initialize_session_state('snowflake_schema_2', get_connection_details(session, 'current_schema()'))
    # initialize_session_state('snowflake_model_1', "")
    # initialize_session_state('snowflake_model_2', "")

    write_connection_details(session)

    # Create before and after columns
    column_widths = [1, 1]
    c1, c2 = st.columns(column_widths)
    c1.subheader("Before")
    c2.subheader("After")
    

    data_source_type_1 = c1.selectbox("Data Source", ["Upload File", "Snowflake Connection"], key = 'c1_selectbox')

    if data_source_type_1 == "Upload File":
        upload_data(file_uploader_key='1', container=c1, session_state_key='df_before')
    elif data_source_type_1 == "Snowflake Connection":
        get_snowflake_model(session, c1, 'snowflake_database_1', 'snowflake_schema_1', 'snowflake_model_1', 'table comparison c1', 'df_before')


    data_source_type_2 = c2.selectbox("Data Source", ["Upload File", "Snowflake Connection"], key = 'c2_selectbox')

    if data_source_type_2 == "Upload File":
        upload_data(file_uploader_key='2', container=c2, session_state_key='df_after')
    elif data_source_type_2 == "Snowflake Connection":
        get_snowflake_model(session, c2, 'snowflake_database_2', 'snowflake_schema_2', 'snowflake_model_2', 'table comparison c2', 'df_after')

    if 'df_before' in st.session_state and 'df_after' in st.session_state:
        # Multiselect for identifying keys
        keys = st.multiselect("Which column(s) are unique keys? (must be the same for both datasets)", st.session_state.df_after.columns)
        if len(keys) > 0:
                
            st.session_state.df_before = st.session_state.df_before.drop_duplicates(subset = keys)
            st.session_state.df_after = st.session_state.df_after.drop_duplicates(subset = keys)
            
            
            #initialize key columns
            st.session_state.df_before['key']=''
            st.session_state.df_after['key']=''
            
            #create new column key which combines all key columns
            for k in keys:
                st.session_state.df_before['key']+=st.session_state.df_before[k].astype(str)
                st.session_state.df_after['key']+=st.session_state.df_after[k].astype(str)

            ## if unique combo is not unique there will be a problem ##

            #gets new and deleted rows
            list1=st.session_state.df_before['key']
            list2=st.session_state.df_after['key']
            new_rows_list, deleted_rows_list = getElementsNotSharedInLists(list1, list2)
            
            #gets new and deleted columns
            list1=st.session_state.df_before.columns
            list2=st.session_state.df_after.columns
            new_cols_list, deleted_cols_list = getElementsNotSharedInLists(list1, list2)

            #set index to new columns 'key'
            st.session_state.df_before = st.session_state.df_before.set_index('key')
            st.session_state.df_after = st.session_state.df_after.set_index('key')

            st.markdown("---")
            ## Three expanders ##

            new_rows_expander = st.expander(label="New Rows", expanded=False)
            with new_rows_expander:
                # show rows that were added to new dataset
                st.dataframe(st.session_state.df_after.loc[new_rows_list, :])

            deleted_rows_expander = st.expander(label="Deleted Rows", expanded=False)
            with deleted_rows_expander:
                # show rows that were deleted from original dataset
                st.dataframe(st.session_state.df_before.loc[deleted_rows_list, :])
                
            changed_rows_expander = st.expander(label="Dataset comparison", expanded=True)
            with changed_rows_expander:
                
                #Copy dataframes excluded rows displayed in previous expanders
                dfc_before = st.session_state.df_before.drop(deleted_rows_list, axis = 0)
                dfc_after = st.session_state.df_after.drop(new_rows_list, axis = 0)
                
                #These lists are for the combined data frame formatting
                new_cols_list_tilda = []
                deleted_cols_list_tilda = []

                #add new columns to dfc_before
                for col in new_cols_list:
                    dfc_before[col] = ''
                    new_cols_list_tilda.append('~' + col + '~')

                #add deleted columns to dfc_after
                for col in deleted_cols_list:
                    dfc_after[col] = ''
                    deleted_cols_list_tilda.append('~' + col + '~')

                #Add '~' before and after column name in dfc_after
                for col in dfc_after.columns:
                    dfc_after = dfc_after.rename(columns={col: "~"+col+"~"}, errors="raise")
                
                st.write('After dataset column names are surrounded by "~"')

                # dfc_both = join dfc_before and dfc_after
                dfc_both = dfc_before.join(dfc_after, how = 'outer')

                #count changes in each row
                dfc_count = 0
                global dfc_is_changed
                dfc_is_changed = dfc_both.copy()
                final_display_col_names = []

                for col in dfc_before.columns:
                    binary_column = np.logical_and(
                        dfc_both[col] != dfc_both["~"+col+"~"]
                        , np.logical_not(
                            np.logical_and(
                                dfc_both[col].isna()
                                , dfc_both["~"+col+"~"].isna()
                            )))

                    dfc_is_changed[col] = binary_column * 1
                    dfc_is_changed["~"+col+"~"] = binary_column * 1
                    
                    if col not in final_display_col_names:
                        final_display_col_names.append(col)
                    if "~"+col+"~" not in final_display_col_names:
                        final_display_col_names.append("~"+col+"~")

                    dfc_count += np.logical_and(
                        dfc_both[col] != dfc_both["~"+col+"~"]
                        , np.logical_not(
                            np.logical_and(
                                dfc_both[col].isna()
                                , dfc_both["~"+col+"~"].isna()
                            )))

                dfc_both["change_count"] = dfc_count
                dfc_both = dfc_both.sort_values(by=["change_count"], ascending=False)
                
                #position deleted and new columns at end of displayed data frame
                for col in deleted_cols_list + new_cols_list:
                    final_display_col_names.remove(col)
                    final_display_col_names.remove('~' + col + '~')
                    final_display_col_names.append(col)
                    final_display_col_names.append('~' + col + '~')


                dfc_both = dfc_both[final_display_col_names]
                
                color_mappings = []
                for col in dfc_both.columns:

                    if col in deleted_cols_list or col in deleted_cols_list_tilda:
                        color_mappings.append("background: gray")
                    elif col in new_cols_list or col in new_cols_list_tilda:
                        color_mappings.append("background: green")
                    else:
                        color_mappings.append("background: red")

                column_color_mappings = pd.Series(color_mappings, index = dfc_both.columns)

                #iterate through each col in dfc_before rearrange and color code
                st.dataframe(
                    dfc_both.style.apply(
                        lambda r: [column_color_mappings.loc[c] if dfc_is_changed.loc[r.name, c] == 1 else "" for c in r.index]
                        , axis = 1
                        )
                )

