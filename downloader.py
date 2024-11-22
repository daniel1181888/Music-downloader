import os
import re
import threading

from pkg_resources import non_empty_lines
from  yt_dlp import YoutubeDL

from main import sanitize_filename
from spotify_client import  SpotifyClient
from metadata import MetadataManager

class Downloader:
    # Class to download music tracks or playlists form spotify urls

    def __init__(self,download_path):
        self.download_path = download_path
        self.spotify = SpotifyClient()
        self.metadata_manager = MetadataManager()


    @staticmethod
    def sanitize_filename(filename):
        # Sanitize filename based on forbidden characters
        return re.sub(r'[^\w\s]', '', filename)

    def download_song(self,song_name,artist_name,album_name):
        # download song based on the song name and artist name
        sanitized_name = self.sanitize_filename(f"{song_name} - {artist_name}")
        output_template = os.path.join(self.download_path, f"{sanitized_name}.%(ext)s")
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_template,
            'quiet': True,
            'no_warnings': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        search_query = f"ytsearch:{song_name} {artist_name}"
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([search_query])
            return os.path.join(self.download_path, f"{sanitized_name}.mp3")
        except Exception as e:
            raise Exception(f"Failed to download '{song_name}' by '{artist_name}': {e}")

    def download_track(self, track_url, update_progress=None):
        # Download a singel track from a spotify URL

        track_info = self.spotify_client.get_track_info(track_url)
        song_name = track_info['name']
        artist_name = track_info['artists'][0]['name']
        album_name = track_info['album']['name']
        album_art_url = track_info['album']['images'][0]['url']

        if update_progress:
            update_progress(0,1)

        file_path = self.download_song(song_name, artist_name)
        self.metadata_manager.add_metadata(file_path, song_name, artist_name, album_name, album_art_url)

        if update_progress:
            update_progress(1, 1)


    def search_tracks(self,query,limit=10):
        # Search for tracks on spotify
        return self.spotify_client.search_tracks(query, limit)