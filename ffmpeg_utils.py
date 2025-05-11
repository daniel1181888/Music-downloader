import os
import zipfile
import subprocess

import requests


def get_ffmpeg_path():
    return "./ffmpeg/bin"


def does_ffmpeg_exist():
    return os.path.exists(get_ffmpeg_path())


def download_ffmpeg():
    print("Downloading FFmpeg...")
    response = requests.get(
        "https://github.com/yt-dlp/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
    )
    if response.status_code != 200:
        raise Exception("Failed to download FFmpeg")

    with open("ffmpeg.zip", "wb") as f:
        f.write(response.content)

    print("Extracting FFmpeg...")
    # Remove the prefix from the filename, effectively extracting the contents without the root directory
    prefix = "ffmpeg-master-latest-win64-gpl/"
    with zipfile.ZipFile("ffmpeg.zip", "r") as zip_ref:
        for file in zip_ref.infolist():
            file.filename = file.filename.replace(prefix, "")
            if file.filename:
                zip_ref.extract(file, "ffmpeg")

    print("Removing FFmpeg zip file...")
    os.remove("ffmpeg.zip")

    print("FFmpeg downloaded and extracted successfully")


def get_ffmpeg_version():
    return subprocess.check_output([get_ffmpeg_path() + "/ffmpeg.exe", "-version"])
