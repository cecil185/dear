import os
import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
import math
from plotly.subplots import make_subplots
import plotly.graph_objects as go

## GET DATA


def app():

    if not os.path.exists("data/main_data.csv"):
        st.subheader("No data")
        st.write(
            "Please upload data by selecting 'Data Upload' in side menu drop down."
        )
    else:
        df = pd.read_csv("data/main_data.csv")

        corr_expander = st.expander(label="Correlation matrix", expanded=False)

        pair_plots_expander = st.expander(label="Pair Plots", expanded=False)

        univariate_expander = st.expander(
            label="Univariate Distributions", expanded=True
        )

        with corr_expander:
            # Can add mask to the correlation matrix later so only the bottom half shows
            dfc = df.corr(method="pearson")
            z = dfc.values.tolist()

            # change each element of z to type string for annotations
            z_text = [[str(round(y, 1)) for y in x] for x in z]

            # set up figure
            fig = ff.create_annotated_heatmap(
                z,
                x=list(dfc.columns),
                y=list(dfc.columns),
                annotation_text=z_text,
                colorscale="agsunset",
            )

            # flip matrix by reversing y axis
            fig["layout"]["yaxis"]["autorange"] = "reversed"

            # add colorbar
            fig["data"][0]["showscale"] = True
            st.plotly_chart(fig)

        with pair_plots_expander:
            ## IF NO BOXES CHECKED THEN MULTI
            st.write("hi")
            # # Next features - correlation matrix and/or pair plots
            # if st.sidebar.button("Generate pair plots for checked IDs"):
            #     features = df.columns[check_box_list]
            #     fig3 = sns.pairplot(data=df, x_vars=features, y_vars=features)
            #     st.sidebar.pyplot(fig3, use_container_width=True)  # display distribution

        with univariate_expander:
            # num_cols = 2
            # fig = make_subplots(
            #     rows=int(math.ceil(len(df.columns) / num_cols)), cols=num_cols
            # )
            # # for i in range(len(df.columns)):
            # # fig = px.histogram(
            # #     df,
            # #     x=df.columns[i],
            # #     y=df.columns[i],
            # #     marginal="rug"
            # #     # hover_data=df.columns,
            # # )
            # fig2 = px.histogram(df, x=df.columns[2])
            #
            # # sns.displot(data=df, x=df.columns[2], bins=30)
            # fig.add_trace(go.Histogram(x=df[df.columns[2]]), row=1, col=2)

            column_widths = [1, 1]
            c1, c2 = st.columns(column_widths)
            c1.subheader("Feature")
            c2.subheader("Distribution")

            check_box_list = []
            for i in range(0, int(math.floor(len(df.columns) / 2))):
                # create histogram chart
                fig2 = sns.displot(data=df, x=df.columns[i], bins=30)
                c1.pyplot(fig2, use_container_width=True)  # display distribution

            for i in range(int(math.floor(len(df.columns) / 2)), len(df.columns)):
                # create histogram chart
                fig2 = sns.displot(data=df, x=df.columns[i], bins=30)
                c2.pyplot(fig2, use_container_width=True)  # display distribution
