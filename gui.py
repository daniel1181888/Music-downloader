import os

from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, filedialog

from config import Config
from downloader import Downloader


class MusicDownloaderGUI:
    def __init__(self, root: tk.Tk):
        # Root Settings
        self.config: Config = Config()
        self.root: tk.Tk = root
        self.root.title("Music Downloader")

        # Initialize the list to track progress bars
        self.active_progress_bars: list[tk.Frame] = []

        # Fixed window size
        self.window_width: int = 1000
        self.window_height: int = 700
        screen_width: int = self.root.winfo_screenwidth()
        screen_height: int = self.root.winfo_screenheight()
        x = (screen_width - self.window_width) // 2
        y = (screen_height - self.window_height) // 2
        self.root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        self.root.wait_visibility()
        self.root.resizable(False, False)

        # Load and resize the background image
        self.background_image: Image.Image = Image.open("imgs/background.jpg")
        self.bg_image_resized: ImageTk.PhotoImage = ImageTk.PhotoImage(
            self.background_image.resize((self.window_width, self.window_height))
        )

        # Create canvas and add background image
        self.canvas = tk.Canvas(
            self.root, width=self.window_width, height=self.window_height
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_image_resized, anchor="nw")

        # Downloader instance
        self.downloader: Downloader | None = None

        # Set up the UI
        self.setup_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.quit)

        # Check if the Spotify credentials are set
        if not self.config.spotify_client_id or not self.config.spotify_client_secret:
            self.open_popup()
        else:
            self.downloader = Downloader(self.config.download_path)

    def quit(self):
        self.config.save()
        if self.downloader:
            self.downloader.shutdown_executor()  # Ensure all tasks are completed
        self.root.quit()

    def setup_ui(self):
        """Set up the main UI components."""
        if not self.config.download_path:
            print("Download path is not set!")
            return
        os.makedirs(self.config.download_path, exist_ok=True)

        # Title Label
        main_label: tk.Label = tk.Label(
            self.canvas,
            text="Music Downloader (by dj fdjesko)",
            fg="white",
            font=("Arial", 16, "bold"),
            bg="#3c3c3c",  # Dark background to improve contrast
            padx=10,  # Padding inside the label
            pady=10,
        )
        main_label.pack(anchor="n", pady=20)

        # Download Section
        self.create_section_label("Spotify URL", x=100, y=80)
        self.entry_url: tk.Entry = self.create_entry(x=100, y=120)

        # Download Button
        download_button: tk.Button = tk.Button(
            self.canvas,
            text="Download",
            fg="white",  # White text for contrast
            bg="#4CAF50",  # Green background for 'Download'
            font=("Arial", 10, "bold"),  # Smaller font size for a more compact button
            padx=10,  # Horizontal padding inside the button
            pady=5,  # Vertical padding inside the button
            command=self.start_download,
        )
        download_button.place(x=100, y=240)

        # Add the entry field with the default path
        self.download_path_entry: tk.Entry = self.create_entry(x=100, y=200)
        # Set the default value
        self.download_path_entry.insert(0, self.config.download_path)

        # Select default path
        select_path: tk.Button = tk.Button(
            self.canvas,
            text="select path",
            fg="white",  # White text for contrast
            bg="#4CAF50",  # Green background for 'Download'
            font=("Arial", 10, "bold"),  # Smaller font size for a more compact button
            padx=10,  # Horizontal padding inside the button
            pady=5,  # Vertical padding inside the button
            command=self.select_path,
        )
        select_path.place(x=100, y=155)

        # Search Section
        self.create_section_label("Search songs on Spotify", x=100, y=300)
        self.search_entry: tk.Entry = self.create_entry(x=100, y=340)

        # Search Button
        search_button: tk.Button = tk.Button(
            self.canvas,
            text="Search",
            fg="white",  # White text for contrast
            bg="#007BFF",  # Blue background for 'Search'
            font=("Arial", 10, "bold"),  # Smaller font size for a more compact button
            padx=10,  # Horizontal padding inside the button
            pady=5,  # Vertical padding inside the button
            command=self.search_songs,
        )
        search_button.place(x=100, y=380)

        # Results Section: Create a canvas with a scrollbar
        self.results_canvas: tk.Canvas = tk.Canvas(
            self.canvas, bg="#3c3c3c", highlightthickness=0
        )
        self.results_scrollbar: tk.Scrollbar = tk.Scrollbar(
            self.canvas, orient="vertical", command=self.results_canvas.yview
        )
        self.results_canvas.configure(yscrollcommand=self.results_scrollbar.set)
        self.results_scrollable_frame: tk.Frame = tk.Frame(
            self.results_canvas, bg="#3c3c3c"
        )  # Frame inside the canvas to hold results
        self.results_canvas.create_window(
            (0, 0), window=self.results_scrollable_frame, anchor="nw"
        )

        # Place the canvas and scrollbar
        self.results_canvas.place(x=100, y=430, width=800, height=150)
        self.results_scrollbar.place(x=900, y=430, height=150)

        # Configure scrolling behavior
        self.results_canvas.bind("<Configure>", self.on_results_canvas_configure)

        # Download Progress Section
        self.create_section_label("Download Progress", x=600, y=80)
        self.download_bars_frame: tk.Frame = tk.Frame(self.canvas, bg="#3c3c3c")
        self.download_bars_frame.place(x=600, y=120)

    def open_popup(self):
        top: tk.Toplevel = tk.Toplevel(self.root)
        top.wait_visibility()
        # Center the popup window relative to the main window
        top.geometry(
            "%dx%d+%d+%d"
            % (
                self.window_width // 2,
                460,  # Reduced height
                self.root.winfo_x() + self.window_width / 4,
                self.root.winfo_y() + self.window_height / 4,
            )
        )
        top.title("Spotify Credentials Required")
        top.transient(self.root)  # Make the window transient (always on top of parent)
        top.grab_set()  # Make the window modal
        top.configure(bg="#3c3c3c")  # Match the main UI's dark theme

        # Header
        header_label = tk.Label(
            top,
            text="Spotify API Credentials Setup",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#3c3c3c",
            pady=5,  # Reduced padding
        )
        header_label.pack(pady=(10, 10))  # Reduced padding

        # Instructions frame
        instructions_frame = tk.Frame(
            top, bg="#3c3c3c", padx=15, pady=5
        )  # Reduced padding
        instructions_frame.pack(fill="both")

        instructions_text = (
            "1. Visit the Spotify Developer Dashboard\n"
            "2. Login with your Spotify account\n"
            "3. Click on 'Create an App'\n"
            "4. Add a name and description\n"
            "5. For the redirect URI, use 'http://127.0.0.1:8000/callback'\n"
            "6. Enable the 'Web API' scope\n"
            "7. Click on 'Create'\n"
            "8. Copy the CLIENT_ID and CLIENT_SECRET and paste them below\n"
        )

        instructions_label = tk.Label(
            instructions_frame,
            text=instructions_text,
            font=("Arial", 11),
            justify="left",
            fg="white",
            bg="#3c3c3c",
            anchor="w",
        )
        instructions_label.pack(fill="x", pady=2)  # Reduced padding

        # Clickable link
        def open_spotify_dashboard():
            import webbrowser

            webbrowser.open("https://developer.spotify.com/dashboard/applications")

        link_frame = tk.Frame(instructions_frame, bg="#3c3c3c")
        link_frame.pack(fill="x", pady=2)  # Reduced padding

        link_button = tk.Button(
            link_frame,
            text="Open Spotify Developer Dashboard",
            font=("Arial", 10, "underline"),
            fg="#1db954",  # Spotify green
            bg="#3c3c3c",
            bd=0,
            cursor="hand2",
            activebackground="#3c3c3c",
            activeforeground="#1ed760",  # Lighter green on hover
            command=open_spotify_dashboard,
        )
        link_button.pack(pady=2)  # Reduced padding

        # Input fields frame
        input_frame = tk.Frame(top, bg="#3c3c3c", padx=15, pady=5)  # Reduced padding
        input_frame.pack(fill="both")

        # Client ID field
        id_label = tk.Label(
            input_frame,
            text="Client ID:",
            fg="white",
            bg="#3c3c3c",
            font=("Arial", 10, "bold"),
            anchor="w",
        )
        id_label.pack(fill="x", pady=(5, 2))  # Reduced padding

        self.client_id_entry = tk.Entry(
            input_frame,
            width=50,
            bg="#555555",
            fg="white",
            insertbackground="white",
            relief="flat",
            bd=1,
        )
        self.client_id_entry.pack(fill="x", pady=(0, 5), ipady=3)  # Reduced padding

        # Client Secret field
        secret_label = tk.Label(
            input_frame,
            text="Client Secret:",
            fg="white",
            bg="#3c3c3c",
            font=("Arial", 10, "bold"),
            anchor="w",
        )
        secret_label.pack(fill="x", pady=(5, 2))  # Reduced padding

        self.client_secret_entry = tk.Entry(
            input_frame,
            width=50,
            bg="#555555",
            fg="white",
            insertbackground="white",
            relief="flat",
            bd=1,
        )
        self.client_secret_entry.pack(fill="x", pady=(0, 5), ipady=3)  # Reduced padding

        # Buttons frame
        button_frame = tk.Frame(top, bg="#3c3c3c", padx=15, pady=10)  # Reduced padding
        button_frame.pack(fill="x")  # Changed from side="bottom" to ensure visibility

        def close_app():
            top.destroy()
            self.root.quit()

        def apply():
            if self.client_id_entry.get() and self.client_secret_entry.get():
                self.config.spotify_client_id = self.client_id_entry.get()
                self.config.spotify_client_secret = self.client_secret_entry.get()
                self.downloader = Downloader(self.config.download_path)
                top.destroy()

        top.protocol("WM_DELETE_WINDOW", close_app)

        # Create two buttons side by side in the button frame
        # Close button
        close_button = tk.Button(
            button_frame,
            text="Close Application",
            command=close_app,
            fg="white",
            bg="#e74c3c",  # Red for closing
            font=("Arial", 10, "bold"),  # Slightly smaller font
            padx=10,  # Reduced padding
            pady=5,  # Reduced padding
            relief="flat",
        )
        close_button.pack(side="left", padx=5)

        # Apply button
        apply_button = tk.Button(
            button_frame,
            text="Apply",
            command=apply,
            fg="white",
            bg="#1db954",  # Spotify green
            font=("Arial", 10, "bold"),  # Slightly smaller font
            padx=15,  # Reduced padding
            pady=5,  # Reduced padding
            relief="flat",
        )
        apply_button.pack(side="right", padx=5)

    def create_section_label(self, text, x, y):
        """Creates a section label with consistent styling."""
        label: tk.Label = tk.Label(
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
        entry: tk.Entry = tk.Entry(
            self.canvas,
            width=50,
            bg="#3c3c3c",
            fg="white",
            font=("Arial", 12),
            insertbackground="white",
        )
        entry.place(x=x, y=y)
        return entry

    def select_path(self):
        """Opens a directory selection dialog and updates the path."""
        folder_path: str = filedialog.askdirectory()
        # Ensure a valid directory is selected
        if folder_path:
            self.config.download_path = folder_path
            self.download_path_entry.delete(0, tk.END)
            # Update entry field
            self.download_path_entry.insert(0, self.config.download_path)

    def start_download(self):
        """Start downloading the song or playlist."""
        url: str = self.entry_url.get()
        download_path: str = self.download_path_entry.get()
        if not download_path:
            download_path = self.config.download_path

        # Ensure path exists
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        self.downloader.download_path = download_path

        if "playlist" in url:
            total_update_progress, total_signal_completion = self.create_progress_bar(
                "Playlist Download"
            )
            # Submit playlist download to the executor
            self.downloader.executor.submit(
                self.downloader.download_playlist,
                url,
                self.create_progress_bar,
                total_update_progress,
                total_signal_completion,
            )
        else:
            track_update_progress, track_signal_completion = self.create_progress_bar(
                "Track Download"
            )
            # Submit single track download to the executor
            self.downloader.executor.submit(
                self.downloader.download_track, url, track_update_progress
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
        # Transparent background
        row_frame: tk.Frame = tk.Frame(self.results_scrollable_frame, bg="#3c3c3c")
        row_frame.pack(fill="x", pady=5, padx=10)

        # Create a rounded label-style button inside the frame
        name = track["name"]
        artist = track["artists"][0]["name"]
        url = track["external_urls"]["spotify"]

        # Add a label to show the song info, without a background (transparent)
        info_label: tk.Label = tk.Label(
            row_frame,
            text=f"{name} by {artist}",
            anchor="w",
            fg="white",
            bg="#3c3c3c",  # Transparent background
            font=("Arial", 12),
        )
        info_label.pack(side="left", padx=10)

        # Create the "Select" button, also with rounded styling
        select_button: tk.Button = tk.Button(
            row_frame,
            text="Select",
            command=lambda: self.set_download_url(url),
            fg="white",
            bg="#1db954",  # Spotify green color for the button
            font=("Arial", 12),
            relief="flat",  # Flat button style
            padx=10,
            pady=5,
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
        frame: tk.Frame = tk.Frame(self.download_bars_frame, bg=None)
        frame.pack(fill="x", pady=5)

        label: tk.Label = tk.Label(
            frame, text=title, anchor="w", fg="white", bg="#3c3c3c"
        )
        label.pack(side="left")

        progress_bar: ttk.Progressbar = ttk.Progressbar(
            frame, orient="horizontal", mode="determinate", length=200
        )
        progress_bar.pack(side="left", padx=5)

        # Store references for cleanup
        self.active_progress_bars.append(frame)  # Ensure this list exists in __init__

        def update_progress(current, total):
            if progress_bar.winfo_exists():
                self.root.after(
                    0, lambda: self._update_progress_bar(progress_bar, current, total)
                )

        def signal_completion():
            if frame.winfo_exists():
                self.root.after(
                    0,
                    lambda: self._signal_completion(frame, label, progress_bar, title),
                )

        return update_progress, signal_completion

    def _update_progress_bar(self, progress_bar, current, total):
        """Update the progress bar safely."""
        # Check if the widget exists
        if progress_bar.winfo_exists():
            progress_bar["maximum"] = total
            progress_bar["value"] = current

    def _signal_completion(self, frame, label, progress_bar, title):
        """Signal the completion of a download safely."""
        if frame.winfo_exists():  # Check if the frame still exists
            frame.config(bg="#3c3c3c")  # Match the background of other UI components
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
