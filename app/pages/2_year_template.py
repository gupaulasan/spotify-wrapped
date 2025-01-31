import datetime
import sqlite3

import pandas as pd
import streamlit as st


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
YEAR = 2024
first_of_the_year = datetime.date(YEAR, 1, 1)
last_of_the_year = datetime.date(YEAR, 12, 31)

st.set_page_config(
    page_title="Spotify Super Wrapped",
    page_icon=":material/play_circle:",
    layout="wide",
)

st.title(f"{YEAR} Spotify Wrapped")

st.write(
    f"This page presents a detailed analysis of your Spotify data for the year {YEAR}."
)

con = sqlite3.connect("data/my_spotify_data.db")
cur = con.cursor()

cur.execute(
    """
    SELECT *
    FROM logs l
    JOIN tracks t USING (track_id)
    WHERE DATETIME(timestamp) >= ? AND DATETIME(timestamp) <= ?
    AND track_id IS NOT NULL
    """,
    (first_of_the_year, last_of_the_year + datetime.timedelta(days=1)),
)

data = cur.fetchall()
columns = [description[0] for description in cur.description]

df = pd.DataFrame(data, columns=columns).sort_values("timestamp")

top_10_artists = df["artist_name"].value_counts().head(10)
group_by_artist = (
    df.groupby("artist_name")["ms_played"].sum().sort_values(ascending=False).head(10)
)

top_artists_text = "\n".join(
    f"{i + 1}. **{artist}**: {format_time(group_by_artist[i])}, across {top_10_artists.loc[artist]} plays"
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
    f"{i + 1}. **{album}**: {format_time(group_by_album[i])}, across {top_10_albums.loc[album]} plays"
    for i, album in enumerate(group_by_album.index[:10])
)

st.write(
    f"## Top 10 albums\n\nHere are your top 10 albums of {YEAR}\n\n{top_albums_text}"
)
