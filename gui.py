import tkinter as tk
from gettext import textdomain
from tkinter import Entry

root = tk.Tk()
root.title("Music Downloader")
root.geometry('1000x800')

# Create a label widget
label = tk.Label(root,text="Music Downloader(by dj fdjesko)",font=("Helvetica",24,"bold"))
label.pack()

label = tk.Label(root,text="Spotify url", font=("Helvetica",15,"bold"))
label.pack()

downloadurl = Entry(root, width = 100)
downloadurl.pack()

label = tk.Label(root,text="Download path", font=("Helvetica",15,"bold"))
label.pack()

downloadpath = Entry(root, width = 100)
downloadpath.pack()

def clicked():
    label.configure(text = "Downloading")

btn = tk.Button(root, text = "download" ,
             fg = "green", command=clicked)

btn.pack()

# Start the GUI event loop
root.mainloop()

