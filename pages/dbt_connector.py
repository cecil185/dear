import streamlit as st
from functions.utils import create_snowflake_connector, DbtProfiles


def app():
    # ################################################
    # Helper Functions
    # ################################################

    def create_db_connection():
        if st.session_state.selected_profile is None:
            return None

        profile_data = DbtProfiles().get(st.session_state.selected_profile)

        if profile_data is None:
            return None

        return create_snowflake_connector(profile_data)

    def fetch_table_names(profilss=None):
        conn = create_db_connection()
        cur = conn.cursor()

        cur.execute(
            "select * from INFORMATION_SCHEMA.TABLES where table_schema != 'INFORMATION_SCHEMA'"
        )
        results = cur.fetchall()
        st.write(results)
        results = [".".join(row[:3]) for row in results]

        st.write(results)
        st.session_state.tables = results

    def process_table():
        # Create Conn
        conn = create_db_connection()
        if conn is None:
            return
        cur = conn.cursor()
        cur.execute(f"select * from {st.session_state.selected_table} limit 100")
        df = cur.fetch_pandas_all()
        st.session_state.table_data = df
        # Get Table INFO

    #################################################
    # Streamlit UI
    #################################################

    with st.sidebar.form("profile_select"):

        st.selectbox(
            "Select a DBT Profile",
            options=[None] + DbtProfiles().list(),
            key="selected_profile",
        )

        st.form_submit_button("Set Profile", on_click=fetch_table_names)

    if len(st.session_state.tables) > 0:
        with st.sidebar.form("db_fetch"):
            st.selectbox("Select Table", st.session_state.tables, key="selected_table")
            st.form_submit_button("Analyze Table ", on_click=process_table)

    #################################################
    # State Vars
    #################################################

    # if "tables" not in st.session_state:
    #     st.session_state.tables = []
    #
    # if "table_data" not in st.session_state:
    #     st.session_state.table_data = None
