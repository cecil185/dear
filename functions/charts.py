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
