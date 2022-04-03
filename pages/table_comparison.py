import numpy as np
import os
import pandas as pd
import streamlit as st

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
                
            changed_rows_expander = st.expander(label="Modified Rows", expanded=False)
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
                
                st.write('After dataset column names are surrounded by "~" (ex. colname -> ~colname~)')

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

