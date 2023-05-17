from dotenv import load_dotenv
import json
import os
import streamlit as st

from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import udf

load_dotenv()

def get_connection_parameters():
    # Read the JSON template
    with open('config_template.json', 'r') as f:
        connection_json = json.load(f)

    # Replace the placeholder with the environment variable value
    for key in connection_json:
        connection_json[key] = os.getenv('SNOWFLAKE_'+key.upper(), '')

    return connection_json

def create_session():
    # Create Snowflake Session object
    if "snowpark_session" not in st.session_state:
        connection_parameters = get_connection_parameters()
        session = Session.builder.configs(connection_parameters).create()
        st.session_state['snowpark_session'] = session
    else:
        session = st.session_state['snowpark_session']
    return session

    # snowflake_environment = session.sql('select current_user(), current_role(), current_database(), current_schema(), current_version(), current_warehouse()').collect()

    # # Current Environment Details
    # st.sidebar.write('Connection Successful')
    # st.sidebar.write('User                        : {}'.format(snowflake_environment[0][0]))
    # st.sidebar.write('Role                        : {}'.format(snowflake_environment[0][1]))
    # st.sidebar.write('Database                    : {}'.format(snowflake_environment[0][2]))
    # st.sidebar.write('Schema                      : {}'.format(snowflake_environment[0][3]))
    # st.sidebar.write('Warehouse                   : {}'.format(snowflake_environment[0][5]))
    # st.sidebar.write('Snowflake version           : {}'.format(snowflake_environment[0][4]))
    
    return session
    # database_name = snowflake_environment[0][2]
    # schema_name = snowflake_environment[0][3]
    # tables = session.sql(f"SHOW TABLES IN {database_name}.{schema_name}").collect()
    # views = session.sql(f"SHOW VIEWS IN {database_name}.{schema_name}").collect()
    
    # # Extract table names and view names
    # table_names = [row['name'] for row in tables]
    # view_names = [row['name'] for row in views]

    # # Union table names and view names
    # tables_views_names = table_names + view_names

    # model = st.selectbox(
    #         "Table or View", tables_views_names
    #     )
    # rows = session.sql(f"SELECT * FROM {database_name}.{schema_name}.{model} LIMIT 10").collect()
    # st.sidebar.write(rows)