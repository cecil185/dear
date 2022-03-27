## create donut chart
##########################################
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

## Plotly univariate distributions
##########################################
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
