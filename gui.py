import tkinter as tk


root = tk.Tk()
root.title("Music Downloader")
root.geometry('1000x800')

# Create a label widget
label = tk.Label(root,text="Music Downloader(by dj fdjesko)",font=("Helvetica",24,"bold"))
label.pack()

# Start the GUI event loop
root.mainloop()