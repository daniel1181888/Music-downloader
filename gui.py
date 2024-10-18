import tkinter as tk
from tkinter import ttk
from turtledemo.penrose import start

from redis.cluster import command

from main import process_playlist

def start_download():
    playlist_url = entry_url.get()
    songs_path = downloadpath.get()
    process_playlist(playlist_url,songs_path, downloadbar=Downloadbar)



root = tk.Tk()
root.title("Music Downloader")
root.geometry('1000x800')

# Create a label widget
label = tk.Label(root,text="Music Downloader(by dj fdjesko)",font=("Helvetica",24,"bold"))
label.pack()

label = tk.Label(root,text="Spotify url", font=("Helvetica",15,"bold"))
label.pack()

entry_url = tk.StringVar()
entry_urlbox = tk.Entry(root, width = 100,textvariable=entry_url)
entry_urlbox.pack()

label = tk.Label(root,text="Download path", font=("Helvetica",15,"bold"))
label.pack()

downloadpath = tk.StringVar()
downloadpath = tk.Entry(root, width = 100, textvariable=downloadpath)
downloadpath.pack()

def clicked():
    label.configure(text = "Downloading")
    start_download()



btn = tk.Button(root, text = "download" ,fg = "green", command=clicked)
btn.pack()

Downloadbar = ttk.Progressbar(
    root,
    orient="horizontal",
    mode="indeterminate",
    length=300
)
Downloadbar.pack(pady=20)



# Start the GUI event loop
root.mainloop()

