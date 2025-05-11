from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyClient:
    def __init__(self, client_id=None, client_secret=None):
        credentials_manager = SpotifyClientCredentials(
            client_id=client_id, client_secret=client_secret
        )
        self.client = Spotify(client_credentials_manager=credentials_manager)

    def get_track_info(self, track_url):
        track_id = track_url.split("/")[-1].split("?")[0]
        return self.client.track(track_id)

    def get_playlist_tracks(self, playlist_url):
        playlist_id = playlist_url.split("/")[-1].split("?")[0]
        playlist = self.client.playlist(playlist_id)
        return playlist["tracks"]["items"]

    def search_tracks(self, query, limit=10):
        results = self.client.search(q=query, type="track", limit=limit)
        return results["tracks"]["items"]
