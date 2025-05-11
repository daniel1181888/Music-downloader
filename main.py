import tkinter as tk

from gui import MusicDownloaderGUI
from ffmpeg_utils import does_ffmpeg_exist, download_ffmpeg

if __name__ == "__main__":
    if not does_ffmpeg_exist():
        print("FFmpeg not found")
        download_ffmpeg()

    root = tk.Tk()
    app = MusicDownloaderGUI(root)
    root.mainloop()
