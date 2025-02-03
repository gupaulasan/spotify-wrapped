import autorootcwd  # noqa
import requests
from requests.auth import HTTPBasicAuth
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET


def get_spotify_token():
    """Fetches an access token from the Spotify API."""
    token_url = "https://accounts.spotify.com/api/token"
    response = requests.post(
        token_url,
        data={"grant_type": "client_credentials"},
        auth=HTTPBasicAuth(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET),
    )

    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception(f"Failed to get token: {response.text}")


def get_artist_info(artist_id, access_token):
    """Fetches artist info from Spotify API"""
    url = f"https://api.spotify.com/v1/artists/{artist_id}"

    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.text)
