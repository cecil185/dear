from pathlib import Path
import os
import pandas as pd
import snowflake.connector
import streamlit as st
from typing import Dict
from yaml import load, SafeLoader


class Error(Exception):
    """Base class for Errors"""

    pass


class BadDbtProfileError(Error):
    """Raised when the defined profile cannot be found"""

    pass


class BadDbtTargetError(Error):
    """Raised when the defined profile cannot be found"""

    pass


class DbtProfiles:

    PATH_DBT_PROFILE = Path.home() / ".dbt" / "profiles.yml"

    def __init__(self):
        pass

    def list(self):
        return list(self._get_profiles().keys())

    def get(self, profile_name: str, target: str = None) -> Dict:

        profiles = self._get_profiles()

        if profile_name not in profiles:
            raise BadDbtProfileError(f"the DBT Profile:{profile_name} was not found ")

        profile = profiles[profile_name]

        target = profile["target"] if target is None else target
        outputs = profile["outputs"]

        if target not in outputs:
            raise BadDbtTargetError(
                f"the specified target was not found in the dbt profile{profile_name}"
            )

        return outputs[target]

    def _get_profiles(self, path=PATH_DBT_PROFILE):
        return load(open(path), Loader=SafeLoader)


def create_snowflake_connector(dbt_profile):

    print(dbt_profile)
    ctx = snowflake.connector.connect(
        user=dbt_profile["user"],
        password=dbt_profile["password"],
        role=dbt_profile["role"],
        account=dbt_profile["account"],
        warehouse=dbt_profile["warehouse"],
        database=dbt_profile["database"],
    )

    return ctx

def initialize_session_state(key, initial_value):
        if key not in st.session_state:
            st.session_state[key] = initial_value
        else: return


def upload_data(file_uploader_key, container, session_state_key = "data"):
    uploaded_file = container.file_uploader("Choose a file", type=["csv", "xlsx",], key=file_uploader_key)
    
    if uploaded_file is not None:
        file_details = os.path.splitext(uploaded_file.name)
        
        # Check the file extension and then load data accordingly
        if file_details[1] == '.csv':
            data = pd.read_csv(uploaded_file)
        elif file_details[1] == '.xlsx':
            data = pd.read_excel(uploaded_file)
        
        st.session_state[session_state_key] = data