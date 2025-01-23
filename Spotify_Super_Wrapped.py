import streamlit as st

st.set_page_config(
    page_title="Spotify Super Wrapped",
    page_icon=":material/play_circle:",
    layout="wide",
)

st.write("# Super Spotify Wrapped")

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
    """
)
