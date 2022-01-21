"""
This file is the framework for generating multiple Streamlit applications
through an object oriented framework.
Code is from https://github.com/prakharrathi25/data-storyteller.git
"""

# Import libraries
import streamlit as st

# Define the multipage class to manage the multiple apps in our program
class MultiPage:
    def __init__(self) -> None:
        """Constructor class to generate a list which will store all our applications as an instance variable."""
        self.pages = []

    def add_page(self, title, func) -> None:

        self.pages.append({"title": title, "function": func})

    def run(self):
        # Drodown to select the page to run
        page = st.sidebar.selectbox(
            "App Navigation", self.pages, format_func=lambda page: page["title"]
        )

        # run the selected app
        page["function"]()
