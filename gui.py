import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from downloader import Downloader
from dotenv import load_dotenv
import os
import threading


class MusicDownloaderGUI:
    def __init__(self, root):
        load_dotenv()
        songs_path = os.getenv("SONGS_PATH") or "./songs/"
        if not os.path.exists(songs_path):
            os.mkdir(songs_path)

        self.root = root
        self.root.title("Music Downloader")
        self.root.geometry('1000x800')

        # Create a canvas and a scrollbar
        self.canvas = tk.Canvas(root)
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.downloader = Downloader(songs_path)
        self.setup_ui()

    def setup_ui(self):
        self.label_style = {"bg": "#4e4e4e", "fg": "white", "font": ("Arial", 12, "bold")}
        self.entry_style = {"bg": "#3c3c3c", "fg": "white", "font": ("Arial", 12), "insertbackground": "white"}

        background_image = Image.open("imgs/background.jpg")
        background_image = background_image.resize((1920, 1080))
        bg_image = ImageTk.PhotoImage(background_image)
        background_label = tk.Label(self.scrollable_frame, image=bg_image)
        background_label.image = bg_image
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        main_label = tk.Label(self.scrollable_frame, text="Music Downloader (by dj fdjesko)", **self.label_style)
        main_label.pack(pady=(20, 10))

        self.setup_ui_download_section()
        self.setup_ui_search_section()
        self.setup_ui_download_bars_section()

    def setup_ui_download_section(self):
        tk.Label(self.scrollable_frame, text="Spotify URL", **self.label_style).pack()
        self.entry_url = tk.Entry(self.scrollable_frame, width=100, **self.entry_style)
        self.entry_url.pack(pady=(20, 10))

        tk.Label(self.scrollable_frame, text="Download Path", **self.label_style).pack(pady=(20, 10))
        self.download_path_entry = tk.Entry(self.scrollable_frame, width=100, **self.entry_style)
        self.download_path_entry.pack()

        tk.Button(self.scrollable_frame, text="Download", fg="green", command=self.start_download).pack(pady=(10, 0))

    def setup_ui_search_section(self):
        tk.Label(self.scrollable_frame, text="Search songs on Spotify", **self.label_style).pack(pady=(20, 10))
        self.search_entry = tk.Entry(self.scrollable_frame, width=100, **self.entry_style)
        self.search_entry.pack(pady=(20, 10))
        tk.Button(self.scrollable_frame, text="Search", fg="blue", command=self.search_songs).pack()

        self.results_frame = tk.Frame(self.scrollable_frame)
        self.results_frame.pack(pady=10)

    def setup_ui_download_bars_section(self):
        tk.Label(self.scrollable_frame, text="Download Progress", **self.label_style).pack(pady=(20, 10))
        self.download_bars_frame = tk.Frame(self.scrollable_frame)
        self.download_bars_frame.pack(fill='x', pady=10)

    def create_progress_bar(self, title):
        frame = tk.Frame(self.download_bars_frame)
        frame.pack(fill='x', pady=5)

        label = tk.Label(frame, text=title, anchor='w')
        label.pack(side='left')

        progress_bar = ttk.Progressbar(frame, orient="horizontal", mode="determinate", length=200)
        progress_bar.pack(side='left', padx=5)

        def update_progress(current, total):
            self.root.after(0, lambda: self._update_progress_bar(progress_bar, current, total))

        def signal_completion():
            self.root.after(0, lambda: self._signal_completion(frame, label, progress_bar, title))

        return update_progress, signal_completion

    def _update_progress_bar(self, progress_bar, current, total):
        progress_bar["maximum"] = total
        progress_bar["value"] = current
        progress_bar.update()

    def _signal_completion(self, frame, label, progress_bar, title):
        label.config(text=f"{title} - Complete!")
        progress_bar.destroy()
        self.root.after(3000, frame.destroy)

    def start_download(self):
        url = self.entry_url.get()
        download_path = self.download_path_entry.get()
        if not download_path:
            download_path = os.getenv("SONGS_PATH") or "./songs/"
        else:
            if not os.path.exists(download_path):
                os.makedirs(download_path)
        self.downloader.download_path = download_path

        if "playlist" in url:
            total_update_progress, total_signal_completion = self.create_progress_bar("Playlist Download")
            threading.Thread(target=self.downloader.download_playlist_async,
                             args=(url, self.create_progress_bar, total_update_progress, total_signal_completion)
                             ).start()
        else:
            track_update_progress, track_signal_completion = self.create_progress_bar("Track Download")
            threading.Thread(target=self.downloader.download_track_async,
                             args=(url, track_update_progress, track_signal_completion)
                             ).start()

    def search_songs(self):
        query = self.search_entry.get()
        results = self.downloader.search_tracks(query)

        for widget in self.results_frame.winfo_children():
            widget.destroy()

        for track in results:
            self.create_result_row(track)

    def create_result_row(self, track):
        row_frame = tk.Frame(self.results_frame)
        row_frame.pack(fill='x', pady=5)

        name = track['name']
        artist = track['artists'][0]['name']
        url = track['external_urls']['spotify']

        info_label = tk.Label(row_frame, text=f"{name} by {artist}", anchor='w')
        info_label.pack(side='left', padx=5)

        select_button = tk.Button(row_frame, text="Select", command=lambda: self.set_download_url(url))
        select_button.pack(side='right', padx=5)

    def set_download_url(self, url):
        self.entry_url.delete(0, tk.END)
        self.entry_url.insert(0, url)