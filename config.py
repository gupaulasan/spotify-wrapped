import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve Spotify credentials
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
