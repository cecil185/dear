import os
import seaborn as sns
import streamlit as st
import plotly.figure_factory as ff
import pandas as pd


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

        check_box_list = []

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

        with univariate_expander:

            # Create title row - 2 columns
            column_widths = [1, 1]
            c1, c2 = st.columns(column_widths)
            c1.subheader("Feature")
            c2.subheader("Distribution")

            # Display rows with 2 columns
            for i in range(len(df.columns)):
                check_box_list.append(None)

                # create histogram chart
                fig2 = sns.displot(data=df, x=df.columns[i], bins=30)

                # create 4 columns - checkbox, name, pie chart, distribution
                c1, c2 = st.columns(column_widths)
                check_box_list[i] = c1.checkbox(df.columns[i])

                c2.pyplot(fig2, use_container_width=True)

                ## Sort columns alphabetically if wanted - problem is the key might be in the middle of the df and you would want it at the start of the df
                # df[sorted(df.columns)]

        with pair_plots_expander:
            ## If no boxes checked then display multi-select
            if sum(check_box_list) == 0:
                features = st.multiselect("Select features for pair plots", df.columns)
            else:
                features = df.columns[check_box_list]

            if len(features) > 0:
                # Create pair plot
                fig3 = sns.pairplot(data=df, x_vars=features, y_vars=features)

                # Display pair plot
                st.pyplot(fig3, use_container_width=True)
