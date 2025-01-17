import datetime
import json

import pandas as pd
import streamlit as st

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

# Set date range
start_date, end_date = st.date_input(
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
