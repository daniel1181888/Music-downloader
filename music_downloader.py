# music_downloader.py

from spotify_client import SpotifyClient
from downloader import Downloader
from metadata import MetadataManager


class MusicDownloader:
    def __init__(self, download_path):
        self.spotify_client = SpotifyClient()
        self.downloader = Downloader(download_path)
        self.metadata_manager = MetadataManager()

    def download_track(self, track_url, progress_callback=None):
        track_info = self.spotify_client.get_track_info(track_url)
        song_name = track_info['name']
        artist_name = track_info['artists'][0]['name']
        album_name = track_info['album']['name']
        album_art_url = track_info['album']['images'][0]['url']

        file_path = self.downloader.download_song(song_name, artist_name)
        self.metadata_manager.add_metadata(file_path, song_name, artist_name, album_name, album_art_url)

        if progress_callback:
            progress_callback(1, 1)

    def download_playlist(self, playlist_url, progress_callback=None):
        tracks = self.spotify_client.get_playlist_tracks(playlist_url)
        total_tracks = len(tracks)
        for idx, item in enumerate(tracks, start=1):
            track = item['track']
            track_url = track['external_urls']['spotify']
            self.download_track(track_url)
            if progress_callback:
                progress_callback(idx, total_tracks)

    def search_tracks(self, query, limit=10):
        return self.spotify_client.search_tracks(query, limit)
