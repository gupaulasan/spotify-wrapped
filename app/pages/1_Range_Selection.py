import datetime
import sqlite3

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def convert_date(date):
    return datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")


sqlite3.register_converter("DATETIME", convert_date)


# Config
st.set_page_config(
    page_title="Spotify Super Wrapped",
    page_icon=":material/play_circle:",
    layout="wide",
)
st.title("Spotify Super Wrapped")
today = datetime.date.today()
# Set date range
s_date, e_date = st.columns([1, 1])
start_date = s_date.date_input(
    "Select the starting date",
    datetime.datetime(2015, 10, 18),
    format="DD/MM/YYYY",
    min_value=datetime.datetime(2015, 10, 18),
)

end_date = e_date.date_input("Select the end date", today, format=("DD/MM/YYYY"))
# Data import
conn = sqlite3.connect("data/my_spotify_data.db")
cur = conn.cursor()

cur.execute(
    """
    SELECT *
    FROM logs l
    JOIN tracks t USING (track_id)
    WHERE DATETIME(timestamp) >= ? AND DATETIME(timestamp) <= ?
    AND track_id IS NOT NULL
    """,
    (start_date, end_date + datetime.timedelta(days=1)),
)
data = cur.fetchall()
columns = [description[0] for description in cur.description]

df = pd.DataFrame(data, columns=columns)
df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y-%m-%dT%H:%M:%SZ")
df = df.sort_values("timestamp")

# Start Streamlit app

df["total_skips"] = df.groupby("track_id")["skipped"].cumsum()

total_plays, total_hours, unique_artists, unique_songs = st.columns(4)
total_plays.metric("Total plays", str(df.shape[0]) + " plays")
total_hours.metric("Total hours", format(df["ms_played"].sum() / 3.6e6, ".0f") + "h")
unique_artists.metric(
    "Unique artists",
    str(df["artist_name"].nunique()) + " artists",
)
unique_songs.metric("Unique songs", str(df["track_id"].nunique()) + " songs")

most_played_artist, most_played_song, most_skipped_song = st.columns(3)

most_played_artist.metric(
    "Most played artist",
    df["artist_name"].value_counts().idxmax(),
    df["artist_name"].value_counts().max().astype(str) + " plays",
    delta_color="off",
)

most_played_song.metric(
    "Most played song",
    df["track_name"].value_counts().idxmax(),
    df["track_name"].value_counts().max().astype(str) + " plays",
    delta_color="off",
)

most_skipped_song.metric(
    "Most skipped song",
    df["track_name"].iloc[df["total_skips"].idxmax()],
    str(df["total_skips"].max()) + " skips",
    delta_color="off",
)

# Compute temporal stats
df["year"] = df["timestamp"].dt.year
df["month"] = df["timestamp"].dt.month

# Compute
year_month_count = df.groupby(["year", "month"]).size()
month_count = year_month_count.groupby("month").mean()
month_sum = (
    df.groupby(["year", "month"])["ms_played"]
    .sum()
    .reset_index(drop=False)
    .groupby("month")["ms_played"]
    .mean()
    / 3_600_000
)  # average minutes per month

mean_plays = (df.shape[0] / df["year"].nunique()) / 12

# Define plots
month_count_plot = go.Figure(
    data=[go.Bar(y=month_count, x=month_count.index, marker_color="#1DB954")],
)

month_count_plot.update_layout(
    xaxis=dict(
        tickvals=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        ticktext=[
            "Jan.",
            "Feb.",
            "Mar.",
            "Apr.",
            "May",
            "Jun.",
            "Jul.",
            "Aug.",
            "Sep.",
            "Oct.",
            "Nov.",
            "Dec.",
        ],
    ),
    title=dict(text="Average plays per month of the year"),
)
month_count_plot.update_xaxes(title_text="Month of the year")
month_count_plot.update_yaxes(title_text="Avg. # of plays")

st.plotly_chart(month_count_plot)

month_sum_plot = go.Figure()
month_sum_plot.add_trace(go.Bar(y=month_sum, x=month_sum.index, marker_color="#1DB954"))
month_sum_plot.update_layout(
    xaxis=dict(
        tickvals=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        ticktext=[
            "Jan.",
            "Feb.",
            "Mar.",
            "Apr.",
            "May",
            "Jun.",
            "Jul.",
            "Aug.",
            "Sep.",
            "Oct.",
            "Nov.",
            "Dec.",
        ],
    ),
    title=dict(text="Average hours played per month of the year"),
)
month_sum_plot.update_xaxes(title_text="Month of the year")
month_sum_plot.update_yaxes(title_text="Avg. hours played")

st.plotly_chart(month_sum_plot)
