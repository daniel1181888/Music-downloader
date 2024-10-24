import threading
import tkinter as tk
from tkinter import ttk
from main import process_playlist

# Initialize global download thread
download_thread = None

# Function to start the download (runs in a separate thread)
def start_download():
    playlist_url = entry_url.get()
    songs_path = downloadpath.get()  # Now correctly fetching the path from StringVar
    process_playlist(playlist_url, songs_path, downloadbar=Downloadbar)

# Function that will be called when the download button is clicked
def clicked():
    global download_thread
    if not download_thread or not download_thread.is_alive():
        download_label.config(text="Downloading...")  # Update the correct label
        # Start the download process in a new thread
        download_thread = threading.Thread(target=start_download)
        download_thread.start()
        check_thread()  # Start checking the thread status

# Function to check the status of the download thread
def check_thread():
    if download_thread.is_alive():
        root.after(100, check_thread)  # Keep checking every 100ms
    else:
        download_label.config(text="Download Complete!")  # Update the correct label

# GUI Setup
root = tk.Tk()
root.title("Music Downloader")
root.geometry('1000x800')

# Create the main label for the application
main_label = tk.Label(root, text="Music Downloader (by dj fdjesko)", font=("Helvetica", 24, "bold"))
main_label.pack()

# Label and entry box for Spotify URL
url_label = tk.Label(root, text="Spotify URL", font=("Helvetica", 15, "bold"))
url_label.pack()

entry_url = tk.StringVar()
entry_urlbox = tk.Entry(root, width=100, textvariable=entry_url)
entry_urlbox.pack()

# Label and entry box for download path
path_label = tk.Label(root, text="Download Path", font=("Helvetica", 15, "bold"))
path_label.pack()

downloadpath = tk.StringVar()  # Now a StringVar to store the path
downloadpathbox = tk.Entry(root, width=100, textvariable=downloadpath)  # Entry box for path
downloadpathbox.pack()

# Label to display download status
download_label = tk.Label(root, text="", font=("Helvetica", 12))  # Unique label for status updates
download_label.pack()

# Download button
btn = tk.Button(root, text="Download", fg="green", command=clicked)
btn.pack()

# Progress bar for downloads
Downloadbar = ttk.Progressbar(
    root,
    orient="horizontal",
    mode="determinate",
    length=300
)
Downloadbar.pack(pady=20)

# Start the GUI event loop
root.mainloop()
