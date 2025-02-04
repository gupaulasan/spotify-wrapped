import streamlit as st

st.set_page_config(
    page_title="Spotify Super Wrapped",
    page_icon=":material/play_circle:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.write("# Spotify Super Wrapped")

st.markdown(
    """
    **Disclaimer:** This is not an official Spotify product.
    
    This project was developed by [Gustavo Santos](https://www.linkedin.com/in/gustavopsantos/) using his own Spotify data for edcuational purposes, with no commercial intent.
    
    ## What is this?
    
    This tool allows you to explore Spotify data from an user account. It is possible to check some stats about the user's listening habits, such as the most played songs, artists, and genres.
    
    This tool also allows one to compare listening habits between different periods of time.
    
    ## How is this different from Spotify Wrapped?
    Spotify Wrapped allows the user to check their listening habits from the past year. Also, it presents only a few stats, such as the most played songs and artists, and the total time spent listening to music.
    
    The idea here is to provide a more detailed analysis, allowing the user to explore their data in a more flexible way. Also, present some unusual stats, such as the most skipped songs, longest listening sessions, and more.
    
    ## Why is this a thing?
    
    This project was thought to be a way for me to practice some skills while still discovering some interesting facts about my listening habits.
    
    The skills I practiced while developing this project were:
    1. Google Cloud Storage and buckets: I stored my data in .csv files in a GCS bucket and accessed it in my code using streamlit`s connection library
    2. SQL: I used SQL to extract and transform data from the JSON files in which the data was originally stored. I prior version of the app used SQL to access and merge data too.
    3. Streamlit: This is my first project using Streamlit. It was a fun experience to learn about how it works and its best practices
    4. `uv` package and project manager: It is a easy to use and fast manager. I developed this project from beggining to end using it and its capabilities
    """
)
