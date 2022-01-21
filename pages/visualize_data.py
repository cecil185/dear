import os
import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st

## GET DATA


def app():

    if not os.path.exists("data/main_data.csv"):
        st.subheader("No data")
        st.write(
            "Please upload data by selecting 'Data Upload' in side menu drop down."
        )
    else:
        df = pd.read_csv("data/main_data.csv")

        column_widths = [1, 1]
        c1, c2 = st.columns(column_widths)
        c1.subheader("Feature")
        c2.subheader("Distribution")

        check_box_list = []
        for i in range(len(df.columns)):
            check_box_list.append(None)
            # create donut chart
            # # fig = px.pie(df_null, values="percent_null", names="TITLE")
            # fig = px.pie(
            #     df_null,
            #     values=[
            #         df_null.iloc[i]["percent_null"],
            #         1 - df_null.iloc[i]["percent_null"],
            #     ],
            #     names=["Null", "Good"],
            #     color_discrete_sequence=["Green", "Red"],
            # )

            # create histogram chart
            fig2 = sns.displot(data=df, x=df.columns[i], bins=30)

            # create 4 columns - checkbox, name, pie chart, distribution
            c1, c2 = st.columns(column_widths)
            check_box_list[i] = c1.checkbox(df.columns[i])

            c2.pyplot(fig2, use_container_width=True)  # display distribution

        # # Next features - correlation matrix and/or pair plots
        # if st.sidebar.button("Generate pair plots for checked IDs"):
        #     features = df.columns[check_box_list]
        #     fig3 = sns.pairplot(data=df, x_vars=features, y_vars=features)
        #     st.sidebar.pyplot(fig3, use_container_width=True)  # display distribution
