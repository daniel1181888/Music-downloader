# gui.py

import threading
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from music_downloader import MusicDownloader
from dotenv import load_dotenv
import os

class MusicDownloaderGUI:
    def __init__(self, root):
        # ensure download folder
        load_dotenv()
        download_path = os.getenv("DOWNLOAD_PATH") or "./songs/"
        if not os.path.exists(download_path):
            os.mkdir(download_path)

        self.root = root
        self.root.title("Music Downloader")
        self.root.geometry('1000x800')
        self.music_downloader = MusicDownloader(download_path)
        self.setup_ui()

    def setup_ui(self):
        # Define styles
        label_style = {"bg": "#4e4e4e", "fg": "white", "font": ("Arial", 12, "bold")}
        entry_style = {"bg": "#3c3c3c", "fg": "white", "font": ("Arial", 12), "insertbackground": "white"}

        # Background image
        background_image = Image.open("imgs/background.jpg")
        background_image = background_image.resize((1920, 1080))
        bg_image = ImageTk.PhotoImage(background_image)
        background_label = tk.Label(self.root, image=bg_image)
        background_label.image = bg_image  # Keep a reference to avoid garbage collection
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Main label
        main_label = tk.Label(self.root, text="Music Downloader (by dj fdjesko)", **label_style)
        main_label.pack(pady=(20, 10))

        # Spotify URL input
        tk.Label(self.root, text="Spotify URL", **label_style).pack()
        self.entry_url = tk.Entry(self.root, width=100, **entry_style)
        self.entry_url.pack(pady=(20, 10))

        # Download path input
        tk.Label(self.root, text="Download Path", **label_style).pack(pady=(20, 10))
        self.download_path_entry = tk.Entry(self.root, width=100, **entry_style)
        self.download_path_entry.pack()

        # Download status label
        self.download_label = tk.Label(self.root, text="", **label_style)
        self.download_label.pack(pady=(20, 10))

        # Download button
        tk.Button(self.root, text="Download", fg="green", command=self.start_download_thread).pack()

        # Progress bar
        self.download_bar = ttk.Progressbar(self.root, orient="horizontal", mode="determinate", length=300)
        self.download_bar.pack(pady=20)

        # Search functionality
        tk.Label(self.root, text="Search songs on Spotify", **label_style).pack(pady=(20, 10))
        self.search_entry = tk.Entry(self.root, width=100, **entry_style)
        self.search_entry.pack(pady=(20, 10))
        tk.Button(self.root, text="Search", fg="blue", command=self.search_songs).pack()
        self.results_text = tk.Text(self.root, width=50, height=15)
        self.results_text.pack(pady=10)

    def start_download_thread(self):
        self.download_label.config(text="Downloading...")
        self.download_thread = threading.Thread(target=self.download)
        self.download_thread.start()
        self.check_download_thread()

    def download(self):
        url = self.entry_url.get()
        download_path = self.download_path_entry.get()
        self.music_downloader.downloader.download_path = download_path

        if "playlist" in url:
            self.music_downloader.download_playlist(url, progress_callback=self.update_progress)
        elif "track" in url:
            self.music_downloader.download_track(url, progress_callback=self.update_progress)
        else:
            self.download_label.config(text="Invalid URL")

    def check_download_thread(self):
        if self.download_thread.is_alive():
            self.root.after(100, self.check_download_thread)
        else:
            self.download_label.config(text="Download Complete!")

    def update_progress(self, current, total):
        self.download_bar["maximum"] = total
        self.download_bar["value"] = current
        self.download_bar.update()

    def search_songs(self):
        query = self.search_entry.get()
        results = self.music_downloader.search_tracks(query)
        self.results_text.delete(1.0, tk.END)
        for track in results:
            name = track['name']
            artist = track['artists'][0]['name']
            url = track['external_urls']['spotify']
            self.results_text.insert(tk.END, f"Track: {name} by {artist}\nURL: {url}\n\n")
