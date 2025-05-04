from concurrent.futures import ThreadPoolExecutor
import os
import re
import threading

from yt_dlp import YoutubeDL
from spotify_client import SpotifyClient
from metadata import MetadataManager

from config import Config


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
        self.config = Config()
        self.download_path = download_path
        self.spotify_client = SpotifyClient(
            client_id=self.config.spotify_client_id,
            client_secret=self.config.spotify_client_secret,
        )
        self.metadata_manager = MetadataManager()
        self.executor = ThreadPoolExecutor(max_workers=10)

    @staticmethod
    def sanitize_filename(filename):
        """
        Sanitize a filename by removing invalid characters.

        Args:
            filename (str): The filename to sanitize.

        Returns:
            str: The sanitized filename.
        """
        return re.sub(r'[<>:"/\\|?*]', "", filename)

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
            "format": "bestaudio/best",
            "outtmpl": output_template,
            "quiet": True,
            "no_warnings": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }
        search_query = f"ytsearch:{song_name} {artist_name}"
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([search_query])
            return os.path.join(self.download_path, f"{sanitized_name}.mp3")
        except Exception as e:
            raise Exception(f"Failed to download '{song_name}' by '{artist_name}': {e}")

    def download_track(self, track_url, update_progress=None):
        """
        Download a single track from a Spotify URL.

        Args:
            track_url (str): The Spotify URL of the track.
            update_progress (function, optional): Function to update progress.
        """
        track_info = self.spotify_client.get_track_info(track_url)
        song_name = track_info["name"]
        artist_name = track_info["artists"][0]["name"]
        album_name = track_info["album"]["name"]
        album_art_url = track_info["album"]["images"][0]["url"]

        if update_progress:
            update_progress(0, 1)

        file_path = self.download_song(song_name, artist_name)
        self.metadata_manager.add_metadata(
            file_path, song_name, artist_name, album_name, album_art_url
        )

        if update_progress:
            update_progress(1, 1)

    def download_playlist(
        self,
        playlist_url,
        create_progress_bar,
        total_update_progress,
        total_signal_completion,
    ):
        """
        Download all tracks in a Spotify playlist URL using the thread pool.

        Args:
            playlist_url (str): The Spotify URL of the playlist.
            create_progress_bar (function): Function to create progress bars.
            total_update_progress (function): Function to update total progress.
            total_signal_completion (function): Function to signal total completion.
        """
        tracks = self.spotify_client.get_playlist_tracks(playlist_url)
        total_tracks = len(tracks)

        # Initialize total progress
        total_update_progress(0, total_tracks)

        completed_tracks = 0

        def track_completed():
            nonlocal completed_tracks
            completed_tracks += 1
            total_update_progress(completed_tracks, total_tracks)
            if completed_tracks == total_tracks:
                total_signal_completion()

        for item in tracks:
            track = item["track"]
            track_url = track["external_urls"]["spotify"]
            song_name = track["name"]
            artist_name = track["artists"][0]["name"]

            # Create progress bar for the track
            track_title = f"{song_name} by {artist_name}"
            track_update_progress, track_signal_completion = create_progress_bar(
                track_title
            )

            # Submit the download task to the thread pool
            self.executor.submit(
                self._download_track_wrapper,
                track_url,
                track_update_progress,
                track_signal_completion,
                track_completed,
            )

    def _download_track_wrapper(
        self, track_url, update_progress, signal_completion, track_completed
    ):
        """
        Wrapper function to download a track and handle completion signals.

        Args:
            track_url (str): The Spotify URL of the track.
            update_progress (function): Function to update progress.
            signal_completion (function): Function to signal per-track completion.
            track_completed (function): Function to signal total playlist progress.
        """
        try:
            self.download_track(track_url, update_progress)
        except Exception as e:
            print(f"Error downloading track: {e}")
        finally:
            signal_completion()
            track_completed()

    def shutdown_executor(self):
        """
        Shutdown the thread pool executor gracefully.
        """
        self.executor.shutdown(wait=True)

    def download_track_async(self, track_url, update_progress, signal_completion):
        """
        Asynchronously download a single track.

        Args:
            track_url (str): The Spotify URL of the track.
            update_progress (function): Function to update progress.
            signal_completion (function): Function to signal completion.
        """

        def run():
            try:
                self.download_track(track_url, update_progress)
            except Exception as e:
                print(f"Error downloading track: {e}")
            finally:
                signal_completion()

        threading.Thread(target=run).start()

    def download_playlist_async(
        self,
        playlist_url,
        create_progress_bar,
        total_update_progress,
        total_signal_completion,
    ):
        """
        Asynchronously download a playlist.

        Args:
            playlist_url (str): The Spotify URL of the playlist.
            create_progress_bar (function): Function to create progress bars.
            total_update_progress (function): Function to update total progress.
            total_signal_completion (function): Function to signal total completion.
        """
        threading.Thread(
            target=self.download_playlist,
            args=(
                playlist_url,
                create_progress_bar,
                total_update_progress,
                total_signal_completion,
            ),
        ).start()

    def search_tracks(self, query, limit=10):
        """
        Search for tracks on Spotify.

        Args:
            query (str): The search query.
            limit (int, optional): The number of tracks to return. Defaults to 10.

        Returns:
            list: A list of track information dictionaries.
        """
        return self.spotify_client.search_tracks(query, limit)
