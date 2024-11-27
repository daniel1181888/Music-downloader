import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from dotenv import load_dotenv
from downloader import Downloader
import threading


class MusicDownloaderGUI:
    def __init__(self, root):
        # Load environment variables
        load_dotenv()
        songs_path = os.getenv("SONGS_PATH") or "./songs/"
        if not os.path.exists(songs_path):
            os.mkdir(songs_path)

        self.root = root
        self.root.title("Music Downloader")

        # Fixed window size
        self.window_width = 1000
        self.window_height = 700
        self.root.geometry(f"{self.window_width}x{self.window_height}")
        self.root.resizable(False, False)

        # Load and resize the background image
        self.background_image = Image.open("imgs/background.jpg")
        self.bg_image_resized = ImageTk.PhotoImage(
            self.background_image.resize((self.window_width, self.window_height))
        )

        # Create canvas and add background image
        self.canvas = tk.Canvas(self.root, width=self.window_width, height=self.window_height)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_image_resized, anchor="nw")

        # Downloader instance
        self.downloader = Downloader(songs_path)

        # Set up the UI
        self.setup_ui()

    def setup_ui(self):
        """Set up the main UI components."""
        # Title Label
        main_label = tk.Label(
            self.canvas,
            text="Music Downloader (by dj fdjesko)",
            fg="white",
            font=("Arial", 16, "bold"),
            bg="#3c3c3c",  # Dark background to improve contrast
            padx=10,  # Padding inside the label
            pady=10
        )
        main_label.place(x=400, y=20)

        # Download Section
        self.create_section_label("Spotify URL", x=100, y=80)
        self.entry_url = self.create_entry(x=100, y=120)

        self.create_section_label("Download Path", x=100, y=160)
        self.download_path_entry = self.create_entry(x=100, y=200)

        tk.Button(
            self.canvas, text="Download", fg="green", command=self.start_download
        ).place(x=100, y=240)

        # Search Section
        self.create_section_label("Search songs on Spotify", x=100, y=300)
        self.search_entry = self.create_entry(x=100, y=340)

        tk.Button(
            self.canvas, text="Search", fg="blue", command=self.search_songs
        ).place(x=100, y=380)


        # Results Section: Create a canvas with a scrollbar
        self.results_canvas = tk.Canvas(self.canvas, bg=None)
        self.results_scrollbar = tk.Scrollbar(self.canvas, orient="vertical", command=self.results_canvas.yview)
        self.results_canvas.configure(yscrollcommand=self.results_scrollbar.set)
        self.results_scrollable_frame = tk.Frame(self.results_canvas,bg=None)  # Frame inside the canvas to hold results
        self.results_canvas.create_window((0, 0), window=self.results_scrollable_frame, anchor="nw")

        # Place the canvas and scrollbar
        self.results_canvas.place(x=100, y=430, width=800, height=150)
        self.results_scrollbar.place(x=900, y=430, height=150)

        # Configure scrolling behavior
        self.results_canvas.bind("<Configure>", self.on_results_canvas_configure)

        # Download Progress Section
        self.create_section_label("Download Progress", x=600, y=80)
        self.download_bars_frame = tk.Frame(self.canvas, bg=None)
        self.download_bars_frame.place(x=600, y=120)

    def create_section_label(self, text, x, y):
        """Creates a section label with consistent styling."""
        label = tk.Label(
            self.canvas,
            text=text,
            fg="white",  # White text color for contrast
            font=("Arial", 12, "bold"),
            bg="#3c3c3c",  # Dark background to improve contrast
            padx=5,  # Add some padding inside the label
            pady=5,
            relief="solid",  # Optional: Adds a border for emphasis
            borderwidth=2
        )
        label.place(x=x, y=y)

    def create_entry(self, x, y):
        """Creates a styled entry field."""
        entry = tk.Entry(
            self.canvas, width=50, bg="#3c3c3c", fg="white", font=("Arial", 12), insertbackground="white"
        )
        entry.place(x=x, y=y)
        return entry

    def start_download(self):
        """Start downloading the song or playlist."""
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
            threading.Thread(
                target=self.downloader.download_playlist_async,
                args=(url, self.create_progress_bar, total_update_progress, total_signal_completion),
            ).start()
        else:
            track_update_progress, track_signal_completion = self.create_progress_bar("Track Download")
            threading.Thread(
                target=self.downloader.download_track_async,
                args=(url, track_update_progress, track_signal_completion),
            ).start()

    def search_songs(self):
        """Search for songs on Spotify."""
        query = self.search_entry.get()
        results = self.downloader.search_tracks(query)

        # Clear previous search results
        for widget in self.results_scrollable_frame.winfo_children():
            widget.destroy()

        # Display search results
        for track in results:
            self.create_result_row(track)

            # Update the scroll region to fit the content
        self.results_canvas.configure(scrollregion=self.results_canvas.bbox("all"))

    def on_results_canvas_configure(self, event):
        """Update the scroll region of the canvas to match the content size."""
        self.results_canvas.configure(scrollregion=self.results_canvas.bbox("all"))

    def create_result_row(self, track):
        """Creates a row for a search result."""
        row_frame = tk.Frame(self.results_scrollable_frame, bg=None)  # Transparent background
        row_frame.pack(fill="x", pady=5, anchor="w")

        name = track["name"]
        artist = track["artists"][0]["name"]
        url = track["external_urls"]["spotify"]

        info_label = tk.Label(row_frame, text=f"{name} by {artist}", anchor="w", fg="white", bg="#3c3c3c")
        info_label.pack(side="left", padx=5)

        select_button = tk.Button(row_frame, text="Select", command=lambda: self.set_download_url(url))
        select_button.pack(side="right", padx=5)

    def set_download_url(self, url):
        """Set the selected song's URL into the entry field."""
        self.entry_url.delete(0, tk.END)
        self.entry_url.insert(0, url)

    def create_progress_bar(self, title):
        """Create and manage a download progress bar."""
        frame = tk.Frame(self.download_bars_frame, bg=None)
        frame.pack(fill="x", pady=5)

        label = tk.Label(frame, text=title, anchor="w", fg="white", bg="#3c3c3c")
        label.pack(side="left")

        progress_bar = ttk.Progressbar(frame, orient="horizontal", mode="determinate", length=200)
        progress_bar.pack(side="left", padx=5)

        def update_progress(current, total):
            self.root.after(0, lambda: self._update_progress_bar(progress_bar, current, total))

        def signal_completion():
            self.root.after(0, lambda: self._signal_completion(frame, label, progress_bar, title))

        return update_progress, signal_completion

    def _update_progress_bar(self, progress_bar, current, total):
        """Update progress bar state."""
        progress_bar["maximum"] = total
        progress_bar["value"] = current
        progress_bar.update()

    def _signal_completion(self, frame, label, progress_bar, title):
        """Signal download completion."""
        label.config(text=f"{title} - Complete!")
        progress_bar.destroy()
        self.root.after(3000, frame.destroy)
