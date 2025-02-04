import os

import streamlit as st
from google.cloud import storage

os.chdir("./")

st.set_page_config(
    page_title="Spotify Super Wrapped",
    page_icon=":material/play_circle:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Configurar credenciais (salve o JSON na pasta do projeto)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "spotify-data-2710-572835308829.json"


def download_db(bucket_name, source_blob_name, destination_file_name):
    """Baixa o banco do Google Cloud Storage"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)


# Baixando o banco
BUCKET_NAME = "spotify-streamlit-app-db"
DB_FILE = "my_spotify_data.db"

download_db(BUCKET_NAME, DB_FILE, DB_FILE)

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
    """
)
