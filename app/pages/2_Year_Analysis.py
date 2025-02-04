import datetime
import sqlite3

import pandas as pd
import streamlit as st
from st_files_connection import FilesConnection


def convert_date(date):
    "Convert a string to a specific formatted date"
    return datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")


def format_time(milliseconds):
    "From milliseconds to written out hours and minutes"
    hours = milliseconds // 3_600_000
    minutes = (milliseconds % 3_600_000) // 60_000
    return f"{hours:.0f}h and {minutes} minutes"


# Create SQL converter
sqlite3.register_converter("DATETIME", convert_date)

# Config
st.set_page_config(
    page_title="Spotify Super Wrapped",
    page_icon=":material/play_circle:",
    layout="wide",
)

year_select, _ = st.columns([1, 2])
YEAR = year_select.selectbox("Select the year you want to analyse", range(2015, 2025))
first_of_the_year = datetime.date(YEAR, 1, 1)
first_of_the_year = pd.to_datetime(first_of_the_year, format="%Y-%m-%dT%H:%M:%SZ")
last_of_the_year = datetime.date(YEAR, 12, 31)
last_of_the_year = pd.to_datetime(last_of_the_year, format="%Y-%m-%dT%H:%M:%SZ")

st.title(f"{YEAR} Stats")

st.write(
    f"This page presents a detailed analysis of your Spotify data for the year {YEAR}."
)

## LEGACY CODE USING SQLite
# conn = sqlite3.connect("my_spotify_data.db")
# cur = conn.cursor()

# cur.execute(
#     """
#     SELECT *
#     FROM logs l
#     JOIN tracks t USING (track_id)
#     WHERE DATETIME(timestamp) >= ? AND DATETIME(timestamp) <= ?
#     AND track_id IS NOT NULL
#     """,
#     (start_date, end_date + datetime.timedelta(days=1)),
# )
# data = cur.fetchall()
# columns = [description[0] for description in cur.description]

# df = pd.DataFrame(data, columns=columns)

# Data import
conn = st.connection("gcs", type=FilesConnection)
logs = conn.read("spotify-streamlit-app-db/logs.csv")
logs["timestamp"] = pd.to_datetime(logs["timestamp"], format="%Y-%m-%dT%H:%M:%SZ")

logs = logs[
    (logs["timestamp"] >= first_of_the_year) & (logs["timestamp"] <= last_of_the_year)
]
tracks = conn.read("spotify-streamlit-app-db/tracks.csv")

df = pd.merge(logs, tracks, on="track_id", suffixes=("_l", "_t"))

df = df.sort_values("timestamp")

top_10_artists = df["artist_name"].value_counts()
group_by_artist = (
    df.groupby("artist_name")["ms_played"].sum().sort_values(ascending=False)
)

top_artists_text = "\n".join(
    f"{i + 1}. **{artist}**: {format_time(group_by_artist.iloc[i])}, across {top_10_artists.loc[artist]} plays"
    for i, artist in enumerate(group_by_artist.index[:10])
)

st.write(
    f"## Top 10 artists\n\nHere are your top 10 artists of {YEAR}\n\n{top_artists_text}"
)

top_10_albums = df["album_name"].value_counts()
group_by_album = (
    df.groupby("album_name")["ms_played"].sum().sort_values(ascending=False)
)

top_albums_text = "\n".join(
    f"{i + 1}. **{album} ({df.loc[lambda df: df['album_name'] == album].iloc[0]['artist_name']})**: {format_time(group_by_album.iloc[i])}, across {top_10_albums.loc[album]} plays"
    for i, album in enumerate(group_by_album.index[:10])
)

st.write(
    f"## Top 10 albums\n\nHere are your top 10 albums of {YEAR}\n\n{top_albums_text}"
)

top_10_tracks = df["track_name"].value_counts()
group_by_track = (
    df.groupby("track_name")["ms_played"].sum().sort_values(ascending=False)
)

top_tracks_text = "\n".join(
    f"{i + 1}. **{track} ({df.loc[lambda df: df['track_name'] == track].iloc[0]['artist_name']})** {format_time(group_by_track.iloc[i])}, across {top_10_tracks.loc[track]} plays"
    for i, track in enumerate(group_by_track.index[:10])
)

st.write(
    f"## Top 10 tracks\n\nHere are yout top 10 tracks of {YEAR}\n\n{top_tracks_text}"
)
