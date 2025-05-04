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
2. **Install Python Dependencies**:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. **Running the Application**
   ```bash
   python main.py
   ```
   You will be prompted to enter your Spotify API credentials. \
   Do as instructed in the GUI.
2. **Using the Application:**
   - Enter a Spotify playlist URL or track URL.
   - Click the "Download" button to start downloading tracks.

## Limitations

- The application does not work for private playlists yet.

## Formatting (for developers)

```bash
black .
```
