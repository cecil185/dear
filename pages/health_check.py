from functions.dataset_ops import getColumnTypes, getNumberNullsByCol
import os
import pandas as pd
import streamlit as st


def app():
    def type_color(type):
        if type == "Categorical":
            return "Orange"
        else:
            return "Blue"

    def null_color(n):
        if n == 0:
            return "Green"
        else:
            return "Red"

    if not os.path.exists("data/main_data.csv"):
        st.subheader("No data")
        st.write(
            "Please upload data by selecting 'Data Upload' in side menu drop down."
        )
    else:
        df = pd.read_csv("data/main_data.csv")

        # Do Work
        #################################################

        (list_type, _, __, ___) = getColumnTypes(df)
        list_nulls = getNumberNullsByCol(df)

        # Error checking
        if len(df.columns) != len(list_nulls) or len(df.columns) != len(list_type):
            st.title("ERROR, length of column names, null, or type lists do not match")

        df_health_info = pd.DataFrame(
            {"TITLE": df.columns, "num_nulls": list_nulls, "data_type": list_type}
        )

        # Display
        #################################################

        my_expander = st.expander(label="View null rows")

        column_widths = [1.5, 0.8, 1]
        c1, c2, c3 = st.columns(column_widths)
        c1.subheader("Feature")
        c2.subheader("Type")
        c3.subheader("Rows with Null")

        check_box_list = []
        for i in range(len(df.columns)):
            check_box_list.append(None)

            # create 3 columns - checkbox & name, type, nulls
            c1, c2, c3 = st.columns(column_widths)
            check_box_list[i] = c1.checkbox(df_health_info.iloc[i]["TITLE"])
            html = (
                '<p style="font-family:sans-serif; color:'
                + type_color(df_health_info.iloc[i]["data_type"])
                + '; font-size: 18px;">'
                + df_health_info.iloc[i]["data_type"]
                + "</p>"
            )

            c2.markdown(html, unsafe_allow_html=True)

            html = (
                '<p style="font-family:sans-serif; color:'
                + null_color(df_health_info.iloc[i]["num_nulls"])
                + '; font-size: 18px;">'
                + str(df_health_info.iloc[i]["num_nulls"])
                + " ("
                + str(round(100 * df_health_info.iloc[i]["num_nulls"] / df.shape[0], 1))
                + "%)</p>"
            )

            c3.markdown(html, unsafe_allow_html=True)

        # Displaying Null Rows in Expandor

        with my_expander:
            # If no boxes are checked then print prompt
            if sum(check_box_list) == 0:
                st.write("Please check at least one box to view null rows")
            else:
                features = df.columns[check_box_list]
                # Initializes null_rows as a list of False's the length of dataframe df
                null_rows = [False] * df.shape[0]
                for f in features:
                    # Adds booleans together for row filtering mechanism
                    null_rows = null_rows + df[f].isnull()
                if sum(null_rows) == 0:
                    st.write("The checked features have no null rows")
                else:
                    # .style.highlight highlights cells in the selected columns which are null
                    st.dataframe(
                        df[null_rows].style.highlight_null(
                            subset=features, null_color="orange"
                        )
                    )

        # Sidebar row duplicates code
        st.sidebar.markdown("---")

        # Multiselect for identifying keys
        keys_for_dups = st.sidebar.multiselect(
            "Which column(s) are unique keys?", df.columns
        )
        if len(keys_for_dups) > 0:
            st.sidebar.markdown(
                f"**{sum(df.duplicated(subset=keys_for_dups))} duplicate records** ({round(sum(df.duplicated(subset=keys_for_dups)) / df.shape[0] * 100, 1)}%)"
            )
