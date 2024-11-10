# downloader.py

import os
import re
from yt_dlp import YoutubeDL


class Downloader:
    def __init__(self, download_path):
        self.download_path = download_path

    @staticmethod
    def sanitize_filename(filename):
        return re.sub(r'[<>:"/\\|?*]', '', filename)

    def download_song(self, song_name, artist_name):
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
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([search_query])
        return os.path.join(self.download_path, f"{sanitized_name}.mp3")

