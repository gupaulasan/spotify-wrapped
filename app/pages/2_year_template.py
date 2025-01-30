import streamlit as st

year = 2000

# Config
st.set_page_config(
    page_title="Spotify Super Wrapped",
    page_icon=":material/play_circle:",
    layout="wide",
)

st.title(f"{year} Spotify Wrapped")

st.write(
    f"This page presents a detailed analysis of your Spotify data for the year {year}."
)
