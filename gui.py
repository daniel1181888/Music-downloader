import tkinter as tk
from main import process_playlist

def start_download():
    playlist_url = entry_url.get()
    process_playlist(playlist_url)

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

downloadpath = tk.Entry(root, width = 100)
downloadpath.pack()

def clicked():
    label.configure(text = "Downloading")
    start_download()


btn = tk.Button(root, text = "download" ,
             fg = "green", command=clicked)

btn.pack()

# Start the GUI event loop
root.mainloop()

