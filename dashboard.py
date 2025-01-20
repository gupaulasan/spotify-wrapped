import datetime
import json

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Spotify Super Wrapped",
    page_icon=":material/play_circle:",
    layout="wide",
)

# Data prep
with open("data/Streaming_History_Audio_2023-2024_8.json") as file:
    data_2324 = json.load(file)

with open("data/Streaming_History_Audio_2024-2025_9.json") as file:
    data_2425 = json.load(file)

df_2324 = pd.DataFrame(data_2324)
df_2425 = pd.DataFrame(data_2425)

df_complete = pd.concat([df_2324, df_2425]).reset_index(drop=True)

df_2024 = df_complete[df_complete["ts"].str.contains("2024")].reset_index(drop=True)
df_2024["ts"] = pd.to_datetime(df_2024["ts"])

df_2024["year"] = df_2024["ts"].dt.year
df_2024["month"] = df_2024["ts"].dt.month
df_2024["day"] = df_2024["ts"].dt.day

df_2024 = df_2024[df_2024["episode_name"].isnull()].reset_index(drop=True)

# App
st.title("Spotify Super Wrapped")
today = datetime.date.today()

date, reset = st.columns([2, 1])
# Set date range
start_date, end_date = date.date_input(
    "Select the period",
    [
        datetime.datetime(2024, 1, 1),
        datetime.datetime(2024, 12, 31),
    ],
    format="DD/MM/YYYY",
)

df_selected = df_2024[
    (df_2024["ts"] >= str(start_date))
    & (df_2024["ts"] <= str(end_date + datetime.timedelta(days=1)))
].reset_index(drop=True)

df_selected["cum_plays"] = df_selected.reset_index(drop=False).index + 1

df_selected["total_skips"] = df_selected.groupby("master_metadata_track_name")[
    "skipped"
].cumsum()

total_plays, total_hours, unique_artists, unique_songs = st.columns(4)
total_plays.metric("Total plays", str(df_selected.shape[0]) + " plays")
total_hours.metric(
    "Total hours", format(df_selected["ms_played"].sum() / 3.6e6, ".0f") + "h"
)
unique_artists.metric(
    "Unique artists",
    str(df_selected["master_metadata_album_artist_name"].nunique()) + " artists",
)
unique_songs.metric(
    "Unique songs", str(df_selected["master_metadata_track_name"].nunique()) + " songs"
)

most_played_artist, most_played_song, most_skipped_song, least_played_artist = (
    st.columns(4)
)

most_played_artist.metric(
    "Most played artist",
    df_selected["master_metadata_album_artist_name"].value_counts().idxmax(),
    df_selected["master_metadata_album_artist_name"].value_counts().max().astype(str)
    + " plays",
    delta_color="off",
)

most_played_song.metric(
    "Most played song",
    df_selected["master_metadata_track_name"].value_counts().idxmax(),
    df_selected["master_metadata_track_name"].value_counts().max().astype(str)
    + " plays",
    delta_color="off",
)

most_skipped_song.metric(
    "Most skipped song",
    df_selected["master_metadata_track_name"].iloc[df_selected["total_skips"].idxmax()],
    str(df_selected["total_skips"].max()) + " skips",
    delta_color="off",
)

least_played_artist.metric(
    "Least played artist",
    df_selected["master_metadata_album_artist_name"].value_counts().idxmin(),
    str(df_selected["master_metadata_album_artist_name"].value_counts().min())
    + " plays",
    delta_color="off",
)

st.write(df_selected)
st.line_chart(
    df_selected.groupby(df_selected["ts"].dt.date).size(),
    x_label="Date",
    y_label="Songs played",
)
st.area_chart(
    df_selected.groupby(df_selected["ts"].dt.date)["cum_plays"].max(),
    x_label="Date",
    y_label="Cumulative songs played",
)
