# Music Downloader

## Prerequisites

1. **Install FFmpeg**:
   - Download FFmpeg from the [official site](https://ffmpeg.org/download.html).
   - Follow these steps to set up FFmpeg on your system:
     - Windows: Add the extracted FFmpeg folder (e.g., `C:\ffmpeg\bin`) to your system's PATH environment variable
     - macOS/Linux: Install FFmpeg using Homebrew or download and configure it manually:
       ```bash
       brew install ffmpeg
       ```
   - Verify the installation by running:
     ```bash
     ffmpeg -version
     ```
   - Ensure FFmpeg is accessible globally
2. **Install Python**:
   - Make sure Python 3.8 or higher is installed on your system. You can download it from [python.org](https://www.python.org/).

## Installation

1. **Clone the Repository**:
   ```
   git clone https://github.com/daniel1181888/Music-downloader.git
   cd Music-downloader
   ```
   Install Python Dependencies:
   ```
   pip install -r requirements.txt
   ```
2. **Set Up Spotify API Credentials:**
   1. Copy the `example.env` file and rename it to `.env`
   2. Visit the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications) and log in with your Spotify account
   3. Click the "Create App" button in the top right corner
   4. Give the app a name and description
   5. For the redirect URI, use `http://localhost:8000`
   6. Enable the `Web API` scope
   7. Click the "Create" button
   8. Copy the `Client ID` and `Client Secret` and paste them into the `.env` file
3. **Running the Application**
   ```bash
   python main.py
   ```
4. **Using the Application:**
   - Enter a Spotify playlist URL or track URL.
   - Click the "Download" button to start downloading tracks.

## Formatting (for developers)

```bash
black .
```
