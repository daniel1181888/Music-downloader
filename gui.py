import json
import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk
import os
from dotenv import load_dotenv


from downloader import Downloader
import threading
import tkinter.filedialog as filedialog


SETTINGS_PATH = "./settings.json"


class MusicDownloaderGUI:
    def __init__(self, root: tk.Tk):

        # Load environment variables
        load_dotenv()

        # Default Settings
        self.songs_path = "songs"

        # Root Settings
        self.root = root
        self.root.title("Music Downloader")

        self.active_progress_bars = []  # Initialize the list to track progress bars

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

        # Load settings
        self.load_settings()

        # Downloader instance
        self.downloader = Downloader(self.songs_path)

        # Set up the UI
        self.setup_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.quit)

    def quit(self):
        self.save_settings()
        self.downloader.shutdown_executor()  # Ensure all tasks are completed
        self.root.quit()

    def load_settings(self):
        """Load settings from the JSON file."""
        if not os.path.exists(SETTINGS_PATH):
            print("Settings file not found")
            return

        with open(SETTINGS_PATH, "r") as f:
            json_data: dict = json.load(f)
            self.songs_path = json_data.get("songs_path", self.songs_path)  # Use .get() to handle missing key
            print("Settings loaded")

    def save_settings(self):
        with open(SETTINGS_PATH, "w") as f:
            data = {
                "songs_path": self.songs_path
            }
            json.dump(data, f, indent=4)
            print("Settings saved")

    def setup_ui(self):
        """Set up the main UI components."""
        if not self.songs_path:
            print("Download path is not set!")
            return
        os.makedirs(self.songs_path, exist_ok=True)


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
        main_label.pack(anchor="n", pady=20)

        # Download Section
        self.create_section_label("Spotify URL", x=100, y=80)
        self.entry_url = self.create_entry(x=100, y=120)


        # Download Button
        download_button = tk.Button(
            self.canvas,
            text="Download",
            fg="white",  # White text for contrast
            bg="#4CAF50",  # Green background for 'Download'
            font=("Arial", 10, "bold"),  # Smaller font size for a more compact button
            padx=10,  # Horizontal padding inside the button
            pady=5,  # Vertical padding inside the button
            command=self.start_download
        )
        download_button.place(x=100, y=240)

        # Add the entry field with the default path
        self.download_path_entry = self.create_entry(x=100, y=200)
        self.download_path_entry.insert(0, self.songs_path)  # Set the default value

        # Select default path
        select_path = tk.Button(
            self.canvas,
            text="select path",
            fg="white",  # White text for contrast
            bg="#4CAF50",  # Green background for 'Download'
            font=("Arial", 10, "bold"),  # Smaller font size for a more compact button
            padx=10,  # Horizontal padding inside the button
            pady=5,  # Vertical padding inside the button
            command=self.select_path
        )
        select_path.place(x=100, y=155)

        # Search Section
        self.create_section_label("Search songs on Spotify", x=100, y=300)
        self.search_entry = self.create_entry(x=100, y=340)

        # Search Button
        search_button = tk.Button(
            self.canvas,
            text="Search",
            fg="white",  # White text for contrast
            bg="#007BFF",  # Blue background for 'Search'
            font=("Arial", 10, "bold"),  # Smaller font size for a more compact button
            padx=10,  # Horizontal padding inside the button
            pady=5,  # Vertical padding inside the button
            command=self.search_songs
        )
        search_button.place(x=100, y=380)


        # Results Section: Create a canvas with a scrollbar
        self.results_canvas = tk.Canvas(self.canvas, bg="#3c3c3c", highlightthickness=0)
        self.results_scrollbar = tk.Scrollbar(self.canvas, orient="vertical", command=self.results_canvas.yview)
        self.results_canvas.configure(yscrollcommand=self.results_scrollbar.set)
        self.results_scrollable_frame = tk.Frame(self.results_canvas,bg="#3c3c3c")  # Frame inside the canvas to hold results
        self.results_canvas.create_window((0, 0), window=self.results_scrollable_frame, anchor="nw")

        # Place the canvas and scrollbar
        self.results_canvas.place(x=100, y=430, width=800, height=150)
        self.results_scrollbar.place(x=900, y=430, height=150)

        # Configure scrolling behavior
        self.results_canvas.bind("<Configure>", self.on_results_canvas_configure)

        # Download Progress Section
        self.create_section_label("Download Progress", x=600, y=80)
        self.download_bars_frame = tk.Frame(self.canvas, bg="#3c3c3c")
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
        )
        label.place(x=x, y=y)

    def create_entry(self, x, y):
        """Creates a styled entry field."""
        entry = tk.Entry(
            self.canvas, width=50, bg="#3c3c3c", fg="white", font=("Arial", 12), insertbackground="white"
        )
        entry.place(x=x, y=y)
        return entry

    def select_path(self):
        """Opens a directory selection dialog and updates the path."""
        folder_path = filedialog.askdirectory()
        if folder_path:  # Ensure a valid directory is selected
            self.songs_path = folder_path
            self.download_path_entry.delete(0, tk.END)
            self.download_path_entry.insert(0, self.songs_path)  # Update entry field

   def start_download(self):
    """Start downloading the song or playlist."""
    url = self.entry_url.get()
    download_path = self.download_path_entry.get()
    if not download_path:
        download_path = self.songs_path

    if not os.path.exists(download_path):  # Ensure path exists
        os.makedirs(download_path)
    self.downloader.download_path = download_path

    if "playlist" in url:
        total_update_progress, total_signal_completion = self.create_progress_bar("Playlist Download")
        # Submit playlist download to the executor
        self.downloader.executor.submit(
            self.downloader.download_playlist,
            url,
            self.create_progress_bar,
            total_update_progress,
            total_signal_completion
        )
    else:
        track_update_progress, track_signal_completion = self.create_progress_bar("Track Download")
        # Submit single track download to the executor
        self.downloader.executor.submit(
            self.downloader.download_track,
            url,
            track_update_progress
        )

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
        """Creates a row for a search result with transparent background and rounded corners."""
        row_frame = tk.Frame(self.results_scrollable_frame, bg="#3c3c3c")  # Transparent background
        row_frame.pack(fill="x", pady=5, padx=10)

        # Create a rounded label-style button inside the frame
        name = track["name"]
        artist = track["artists"][0]["name"]
        url = track["external_urls"]["spotify"]

        # Add a label to show the song info, without a background (transparent)
        info_label = tk.Label(
            row_frame,
            text=f"{name} by {artist}",
            anchor="w",
            fg="white",
            bg="#3c3c3c",  # Transparent background
            font=("Arial", 12)
        )
        info_label.pack(side="left", padx=10)

        # Create the "Select" button, also with rounded styling
        select_button = tk.Button(
            row_frame,
            text="Select",
            command=lambda: self.set_download_url(url),
            fg="white",
            bg="#1db954",  # Spotify green color for the button
            font=("Arial", 12),
            relief="flat",  # Flat button style
            padx=10,
            pady=5
        )
        select_button.pack(side="right", padx=5)

        # Apply rounded corners effect for the row and the button
        self.make_rounded(row_frame)
        self.make_rounded(select_button)

    def make_rounded(self, widget):
        """Apply rounded corners effect to a widget."""
        widget.config(highlightbackground="black", highlightcolor="black", bd=0)
        widget.update_idletasks()

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

        # Store references for cleanup
        self.active_progress_bars.append(frame)  # Ensure this list exists in __init__

        def update_progress(current, total):
            if progress_bar.winfo_exists():
                self.root.after(0, lambda: self._update_progress_bar(progress_bar, current, total))

        def signal_completion():
            if frame.winfo_exists():
                self.root.after(0, lambda: self._signal_completion(frame, label, progress_bar, title))

        return update_progress, signal_completion

    def _update_progress_bar(self, progress_bar, current, total):
        """Update the progress bar safely."""
        if progress_bar.winfo_exists():  # Check if the widget exists
            progress_bar["maximum"] = total
            progress_bar["value"] = current

    def _signal_completion(self, frame, label, progress_bar, title):
        """Signal the completion of a download safely."""
        if frame.winfo_exists():  # Check if the frame still exists
            frame.config(bg="#3c3c3c")  # Match the background of other UI components
        if label.winfo_exists():  # Check if the label exists
            label.config(fg="green", text=f"{title} - Completed")
        if progress_bar.winfo_exists():  # Check if the progress bar exists
            progress_bar.destroy()

    def cleanup_widgets(self, frame):
        """Clean up a widget safely."""
        # Cancel all associated callbacks
        self.root.after_cancel(self.root)  # Cancel callbacks if you store references

        # Destroy the frame
        if frame.winfo_exists():
            frame.destroy()
