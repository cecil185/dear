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

def create_snowflake_session():
    # Create Snowflake Session object
    if "snowpark_session" in st.session_state:
        session = st.session_state['snowpark_session']
        
    else: 
        connection_parameters = get_connection_parameters()
        session = Session.builder.configs(connection_parameters).create()
        st.session_state['snowpark_session'] = session
        session.use_warehouse('compute_wh')
        
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


def get_snowflake_model(session, container, database_key, schema_key, model_key, button_key, session_state_key='data'):
    
    database = get_connection_details(session, 'current_database()')
    database_input = container.text_input("Database", placeholder=database, key=database_key)
    if database_input and database_input != st.session_state[database_key]:
        st.session_state[database_key] = database_input
        database = database_input

    schema = get_connection_details(session, 'current_schema()')
    schema_input = container.text_input("Schema", placeholder=schema, key=schema_key)
    if schema_input and schema_input != st.session_state[schema_key]:
        st.session_state[schema_key] = schema_input
        schema = schema_input

    model = st.session_state.get(model_key, "")
    model_input = container.text_input("Model", placeholder=model, key=model_key)
    # model_input = container.text_input("Model", placeholder="", key=model_key)
    if model_input and model_input != st.session_state[model_key]:
        st.session_state[model_key] = model_input
        model = model_input
    
    if container.button("Query Database", key=button_key):
        try:
            query = f"SELECT * FROM {database}.{schema}.{model}"
            st.write(query)
            df = session.sql(query).fetch_pandas_all()
            st.session_state[session_state_key] = df
        except:
            st.write("Query failed. Please check your inputs.")

def get_connection_details(session, variable):
    try:
        return session.sql('select ' + variable).collect()[0][0]
    except:
        return ""

def write_connection_details(session):
    st.markdown("""---""")

    # Current Environment Details
    st.write('Connection Successful')
    st.write('User                        : {}'.format(get_connection_details(session, 'current_user()')))
    st.write('Role                        : {}'.format(get_connection_details(session, 'current_role()')))
    st.write('Warehouse                   : {}'.format(get_connection_details(session, 'current_warehouse()')))

    st.markdown("""---""")