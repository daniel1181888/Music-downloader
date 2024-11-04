import threading
import tkinter as tk
from tkinter import ttk
from tkinter.tix import WINDOW
from redis.cluster import command
from main import analyzeUrl
from main import searchsong
from PIL import Image, ImageTk

# Initialize global download thread
download_thread = None

# Function to start the download (runs in a separate thread)
def start_download():
    playlist_url = entry_url.get()
    songs_path = downloadpath.get()  # Now correctly fetching the path from StringVar
    analyzeUrl(playlist_url, songs_path, downloadbar=Downloadbar)

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

def searchsongclicked():

    song_name = search_labelbox.get()  # Get the song name from the entry box
    results_text.delete(1.0, tk.END)  # Clear previous results

    for track in searchsong(song_name):
        results_text.insert(tk.END, F"{track}\n")




# GUI Setup
root = tk.Tk()
root.title("Music Downloader")
root.geometry('1000x800')

#Styling
label_style = {"bg": "#4e4e4e", "fg": "white", "font": ("Arial", 12, "bold")}
entry_style = {"bg": "#3c3c3c", "fg": "white", "font": ("Arial", 12), "insertbackground": "white"}

#load background
background_image = Image.open("imgs/1920x1080-aesthetic-glrfk0ntspz3tvxg.jpg")
background_image = background_image.resize((1000,800))
bg_image = ImageTk.PhotoImage(background_image)

# Create a label for background
# Create a Label for the background
background_label = tk.Label(root, image=bg_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create the main label for the application
main_label = tk.Label(root, text="Music Downloader (by dj fdjesko)", **label_style)
main_label.pack(pady=(20, 10))

# Label and entry box for Spotify URL
url_label = tk.Label(root, text="Spotify URL", **label_style)
url_label.pack()

entry_url = tk.StringVar()
entry_urlbox = tk.Entry(root, width=100, textvariable=entry_url, **entry_style)
entry_urlbox.pack(pady = (20, 10))

# Label and entry box for download path
path_label = tk.Label(root, text="Download Path", **label_style)
path_label.pack(pady=(20, 10))

downloadpath = tk.StringVar()  # Now a StringVar to store the path
downloadpathbox = tk.Entry(root, width=100, textvariable=downloadpath, **label_style)  # Entry box for path
downloadpathbox.pack()

# Label to display download status
download_label = tk.Label(root, text="", **label_style)  # Unique label for status updates
download_label.pack(pady=(20, 10))

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


search_label = tk.Label(root, text="Search songs on spotify", **label_style)
search_label.pack(pady=(20, 10))

search_labelbox = tk.StringVar()
search_labelbox = tk.Entry(root, width=100, textvariable=search_labelbox, **entry_style)
search_labelbox.pack(pady=(20, 10))

btn = tk.Button(root, text="Search", fg="blue", command=searchsongclicked)
btn.pack()

results_text = tk.Text(root, width=50, height=15)
results_text.pack(pady=10)


# Start the GUI event loop
root.mainloop()
