# Music Downloader

## Prerequisites

1. **Install FFmpeg**:
   - Download FFmpeg from the [official site](https://ffmpeg.org/download.html).
   - Follow these steps to set up FFmpeg on your system:
     - Windows: Add the extracted FFmpeg folder (e.g., `C:\ffmpeg\bin`) to your system's PATH environment variable.
     - macOS/Linux: Install FFmpeg using Homebrew or download and configure it manually:
       ```bash
       brew install ffmpeg
       ```
   - Verify the installation by running:
     ```bash
     ffmpeg -version
     ```
   - Ensure FFmpeg is accessible globally.

2. **Install Python**:
   - Make sure Python 3.8 or higher is installed on your system. You can download it from [python.org](https://www.python.org/).

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/daniel1181888/Music-downloader.git
   cd Music-downloader
   ```
    Install Python Dependencies:
        Install the required Python libraries using pip:
    ```bash
    pip install -r requirements.txt
    ```
Set Up Spotify API Credentials:

    Create a .env file in the root directory:
    plaintext

        CLIENT_ID=your_spotify_client_id
        CLIENT_SECRET=your_spotify_client_secret

        Replace your_spotify_client_id and your_spotify_client_secret with your Spotify Developer credentials. You can obtain these by creating an app at the Spotify Developer Dashboard.

Running the Application

    Run the Program:
        Start the Music Downloader GUI:
        bash

    python main.py

Using the Application:

    Enter a Spotify playlist URL or track URL.
    Click the "Download" button to start downloading tracks.

