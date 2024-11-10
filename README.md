Install instructions:
============================

## For Windows:

You can download FFmpeg from the official site: https://ffmpeg.org/download.html
Recommended Option
Download the ffmpeg-master-latest-win64-gpl-shared.zip file (63.9 MB).
https://github.com/BtbN/FFmpeg-Builds/releases
After downloading and extracting FFmpeg, you'll need to add it to your system's PATH environment variable. This allows yt-dlp to find it.
For Windows:

- Locate the folder where you extracted FFmpeg (it should contain ffmpeg.exe, ffprobe.exe, etc.).
- Copy the path to this folder (e.g., C:\ffmpeg\bin).
- Right-click on "This PC" or "My Computer" and select Properties.
- Click on Advanced system settings.
- In the System Properties window, click the Environment Variables button.
- In the System variables section, find the Path variable, select it, and click Edit.
- Click New and paste the path to the FFmpeg bin folder.
- Click OK to close all dialogs.

// TODO: add instructions for installing other dependancies, as for Linux 

## For Linux:
	1. Simply install ffmpeg by doing `sudo apt install ffmpeg` (or a similar command if not using `apt`)
	2. other dependancies: `pip install spotipy yt_dlp mutagen requests Pillow python-dotenv`
	   // TODO: Make sure these can be installed through requirements.txt `pip install -r requirements.txt`

## For MacOS:
If you're using Homebrew, you can install FFmpeg by running:
brew install ffmpeg
// TODO: add instructions for installing other dependancies, as for Linux 

Verify FFmpeg Installation:
============================

Open a command prompt or terminal window.
Type ffmpeg -version and press Enter.
If it’s installed correctly, you should see version information for FFmpeg.

Setting up the spotify API
===========================
1. Go to the (Spotify Developer Dashboard)[https://developer.spotify.com/dashboard]
2. Create an app
	- Choose name and description as desired
	- Set Redirect URI: does not matter (as of yet), you can set it to https://google.com or https://example.org/callback
	- Enable the Web API. The others are not required (as of yet)
3. On the dashboard, your new app is now listed. Open it, and open its settings
4. Create a .env file from the .example.env file (`cp .example.env .env`)
5. Copy the client id and secret from the app settings on the dashboard, into your .env file

Running the music downloader
====================================
TODO: Replace the chatgpt stuff with actual instructions
After completing the steps above, try running your Python script again. It should be able to find FFmpeg and process the audio files without throwing the previous error.
