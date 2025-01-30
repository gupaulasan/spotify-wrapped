"""
This script creates, loads, and saves a database with Spotify data.
"""

import json
import os
import sqlite3

from tqdm import tqdm

# Database and data directory
DB_PATH = "data/my_spotify_data.db"
DATA_DIR = "data"
data_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".json")]

# Connect to SQLite database
with sqlite3.connect(DB_PATH) as con:
    cur = con.cursor()

    # Create tables if they don't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            timestamp TEXT, 
            ms_played INTEGER, 
            track_id TEXT, 
            reason_start TEXT, 
            reason_end TEXT, 
            shuffle BOOLEAN, 
            skipped BOOLEAN, 
            offline BOOLEAN, 
            incognito_mode BOOLEAN
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tracks (
            track_id TEXT PRIMARY KEY, 
            track_name TEXT, 
            artist_name TEXT, 
            album_name TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS podcasts (
            podcast_id TEXT PRIMARY KEY, 
            name TEXT, 
            show TEXT
        )
    """)

    # Process files
    for file in (pbar := tqdm(data_files, desc="Processing files")):
        file_path = os.path.join(DATA_DIR, file)

        with open(file_path, encoding="utf-8") as f:
            content = json.load(f)

        log_entries, track_entries, podcast_entries = [], [], []

        for line in content:
            ts = line.get("ts")
            ms_played = line.get("ms_played", 0)
            reason_start = line.get("reason_start")
            reason_end = line.get("reason_end")
            shuffle = line.get("shuffle", False)
            skipped = line.get("skipped", False)
            offline = line.get("offline", False)
            incognito_mode = line.get("incognito_mode", False)

            track_name = line.get("master_metadata_track_name", "Unknown")
            artist_name = line.get("master_metadata_album_artist_name", "Unknown")
            album_name = line.get("master_metadata_album_album_name", "Unknown")

            podcast_name = line.get("episode_show_name", "Unknown")
            episode_name = line.get("episode_name", "Unknown")

            # Extract track ID
            track_uri = line.get("spotify_track_uri")
            track_id = track_uri.split(":")[2] if track_uri else None

            # Extract podcast ID
            episode_uri = line.get("spotify_episode_uri")
            podcast_id = episode_uri.split(":")[2] if episode_uri else None

            # Add track entry if track exists
            if track_id:
                track_entries.append((track_id, track_name, artist_name, album_name))

            # Add podcast entry if podcast exists
            if podcast_id:
                podcast_entries.append((podcast_id, episode_name, podcast_name))

            # Add log entry
            log_entries.append(
                (
                    ts,
                    ms_played,
                    track_id,
                    reason_start,
                    reason_end,
                    shuffle,
                    skipped,
                    offline,
                    incognito_mode,
                )
            )

        # Insert records using batch processing
        cur.executemany(
            """
            INSERT OR IGNORE INTO tracks (track_id, track_name, artist_name, album_name) 
            VALUES (?, ?, ?, ?)
        """,
            track_entries,
        )

        cur.executemany(
            """
            INSERT OR IGNORE INTO podcasts (podcast_id, name, show) 
            VALUES (?, ?, ?)
        """,
            podcast_entries,
        )

        cur.executemany(
            """
            INSERT INTO logs (timestamp, ms_played, track_id, reason_start, reason_end, shuffle, skipped, offline, incognito_mode) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            log_entries,
        )

    # Commit all changes
    con.commit()
