#!/usr/bin/env python3

from gui import MusicDownloaderGUI
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicDownloaderGUI(root)
    root.mainloop()
