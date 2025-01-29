"""
This file crates, loads and saves the database with Spotify data.
"""

import json
import os
import sqlite3

from tqdm import tqdm

data_dir = "data"
data_files = os.listdir(data_dir)
print(data_files)
# Connect to the database
con = sqlite3.connect("data/my_spotify_data.db")
cur = con.cursor()

# Create the tables
cur.execute("""
               CREATE TABLE IF NOT EXISTS logs(log_id INTEGER PRIMARY KEY ASC, timestamp, ms_played, track_id, reason_start, reason_end, shuffle BOOL, skipped BOOL, offline BOOL, incognito_mode BOOL)
               """)

cur.execute("""
                CREATE TABLE IF NOT EXISTS tracks(track_id TEXT PRIMARY KEY, track_name TEXT, artist_name TEXT, album_name TEXT)
            """)

cur.execute("""
                CREATE TABLE IF NOT EXISTS podcasts(podcast_id TEXT PRIMARY KEY, name TEXT, show TEXT)
            """)

# Populate the tables
tracks = []
podcasts = []
for file in (pbar := tqdm(data_files)):
    pbar.set_description(f"Processing {file}")
    if ".json" in file:
        with open(os.path.join(data_dir, file)) as f:
            content = json.load(f)
            for line in content:
                ts = line["ts"]
                ms_played = line["ms_played"]
                reason_start = line["reason_start"]
                reason_end = line["reason_end"]
                shuffle = line["shuffle"]
                skipped = line["skipped"]
                offline = line["offline"]
                incognito_mode = line["incognito_mode"]
                track_name = line["master_metadata_track_name"]
                artist_name = line["master_metadata_album_artist_name"]
                album_name = line["master_metadata_album_album_name"]
                podcast_name = line["episode_show_name"]
                episode_name = line["episode_name"]

                track_uri = line["spotify_track_uri"]
                if track_uri is not None:
                    track_uri = track_uri.split(":")[2]

                    if track_uri not in tracks:
                        cur.execute(
                            "INSERT INTO tracks(track_id, track_name, artist_name, album_name) VALUES(?, ?, ?, ?)",
                            (track_uri, track_name, artist_name, album_name),
                        )
                        tracks.append(track_uri)

                episode_uri = line["spotify_episode_uri"]
                if episode_uri is not None:
                    episode_uri = episode_uri.split(":")[2]
                    if episode_uri not in podcasts:
                        cur.execute(
                            "INSERT INTO podcasts(name, show, podcast_id) VALUES(?, ?, ?)",
                            (episode_name, podcast_name, episode_uri),
                        )
                        podcasts.append(episode_uri)

                cur.execute(
                    "INSERT INTO logs(timestamp, ms_played, track_id, reason_start, reason_end, shuffle, skipped, offline, incognito_mode) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        ts,
                        ms_played,
                        track_uri,
                        reason_start,
                        reason_end,
                        shuffle,
                        skipped,
                        offline,
                        incognito_mode,
                    ),
                )

# Commit the changes
con.commit()
# Close the connection
con.close()
