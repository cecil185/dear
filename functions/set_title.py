import os
import pandas as pd
import streamlit as st


def set():
    # Title of the main page
    c1, c2, c3 = st.columns((1, 3, 3))
    c1.image("data/deer_logo.jpeg", use_column_width=True)
    c2.markdown("### Stealth Project DEAR")
    if os.path.exists("data/uploaded_file_name.txt"):
        c3.markdown(f"##### {open('data/uploaded_file_name.txt', 'r').read()}")
        if os.path.exists("data/main_data.csv"):
            df = pd.read_csv("data/main_data.csv")
            c3.write(f"{int(os.path.getsize('data/main_data.csv') / 1000)} MB")
            c3.write(str(df.shape[0]) + " records x " + str(df.shape[1]) + " features")

    st.markdown("""---""")
