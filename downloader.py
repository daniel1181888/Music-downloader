# downloader.py

import os
import re
import threading
from yt_dlp import YoutubeDL
from spotify_client import SpotifyClient
from metadata import MetadataManager

class Downloader:
    """
    Class to download music tracks or playlists from Spotify URLs.
    Handles downloading from YouTube, adding metadata, and threading.
    """

    def __init__(self, download_path):
        """
        Initialize the Downloader with a specified download path.

        Args:
            download_path (str): The directory where songs will be downloaded.
        """
        self.download_path = download_path
        self.spotify_client = SpotifyClient()
        self.metadata_manager = MetadataManager()

    @staticmethod
    def sanitize_filename(filename):
        """
        Sanitize a filename by removing invalid characters.

        Args:
            filename (str): The filename to sanitize.

        Returns:
            str: The sanitized filename.
        """
        return re.sub(r'[<>:"/\\|?*]', '', filename)

    def download_song(self, song_name, artist_name):
        """
        Download a song from YouTube based on the song name and artist name.

        Args:
            song_name (str): The name of the song.
            artist_name (str): The name of the artist.

        Returns:
            str: The path to the downloaded MP3 file.

        Raises:
            Exception: If the download fails.
        """
        sanitized_name = self.sanitize_filename(f"{song_name} - {artist_name}")
        output_template = os.path.join(self.download_path, f"{sanitized_name}.%(ext)s")
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_template,
            'quiet': True,
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

    def download_track(self, track_url, progress_callback=None):
        """
        Download a single track from a Spotify URL.

        Args:
            track_url (str): The Spotify URL of the track.
            progress_callback (function, optional): A callback function to update progress.

        If progress_callback is provided, it will be called with (current, total).

        Raises:
            Exception: If the download fails.
        """
        try:
            track_info = self.spotify_client.get_track_info(track_url)
            song_name = track_info['name']
            artist_name = track_info['artists'][0]['name']
            album_name = track_info['album']['name']
            album_art_url = track_info['album']['images'][0]['url']

            file_path = self.download_song(song_name, artist_name)
            self.metadata_manager.add_metadata(file_path, song_name, artist_name, album_name, album_art_url)

            if progress_callback:
                progress_callback(1, 1)
        except Exception as e:
            raise Exception(f"Failed to download track: {e}")

    def download_playlist(self, playlist_url, progress_callback=None):
        """
        Download all tracks in a Spotify playlist URL.

        Args:
            playlist_url (str): The Spotify URL of the playlist.
            progress_callback (function, optional): A callback function to update progress.

        If progress_callback is provided, it will be called with (current, total) after each track.

        Raises:
            Exception: If the download fails.
        """
        try:
            tracks = self.spotify_client.get_playlist_tracks(playlist_url)
            total_tracks = len(tracks)
            for idx, item in enumerate(tracks, start=1):
                track = item['track']
                track_url = track['external_urls']['spotify']
                self.download_track(track_url)
                if progress_callback:
                    progress_callback(idx, total_tracks)
        except Exception as e:
            raise Exception(f"Failed to download playlist: {e}")

    def search_tracks(self, query, limit=10):
        """
        Search for tracks on Spotify.

        Args:
            query (str): The search query.
            limit (int, optional): The number of tracks to return. Defaults to 10.

        Returns:
            list: A list of track information dictionaries.

        Raises:
            Exception: If the search fails.
        """
        try:
            return self.spotify_client.search_tracks(query, limit)
        except Exception as e:
            raise Exception(f"Failed to search tracks: {e}")

    def download(self, url, progress_callback=None):
        """
        Download a track or playlist from a Spotify URL.

        Args:
            url (str): The Spotify URL of the track or playlist.
            progress_callback (function, optional): A callback function to update progress.

        Determines whether the URL is a track or playlist and downloads accordingly.

        If progress_callback is provided, it will be called with (current, total).

        Raises:
            ValueError: If the URL is invalid.
        """
        if "playlist" in url:
            self.download_playlist(url, progress_callback)
        elif "track" in url:
            self.download_track(url, progress_callback)
        else:
            raise ValueError("Invalid URL")

    def download_async(self, url, progress_callback=None, completion_callback=None):
        """
        Asynchronously download a track or playlist from a Spotify URL.

        Args:
            url (str): The Spotify URL of the track or playlist.
            progress_callback (function, optional): A callback function to update progress.
            completion_callback (function, optional): A callback function called when download completes.

        Starts a new thread to perform the download.

        If progress_callback is provided, it will be called with (current, total).
        If completion_callback is provided, it will be called when download is complete.
        """
        thread = threading.Thread(target=self._download_thread, args=(url, progress_callback, completion_callback))
        thread.start()

    def _download_thread(self, url, progress_callback, completion_callback):
        """
        Internal method to run the download in a separate thread.

        Args:
            url (str): The Spotify URL of the track or playlist.
            progress_callback (function): A callback function to update progress.
            completion_callback (function): A callback function called when download completes.
        """
        try:
            self.download(url, progress_callback)
            if completion_callback:
                completion_callback(success=True)
        except Exception as e:
            if completion_callback:
                completion_callback(success=False, error=str(e))

