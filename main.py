import os.path
from os import path
import re  # For sanitizing filenames
from tkinter.ttk import Progressbar
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC, error
import yt_dlp
from dotenv import load_dotenv
import os



load_dotenv()

# SONGS_PATH = path.join(path.dirname(__file__), "songs")



# Make sure that the songs directory exists
# if not os.path.exists(SONGS_PATH):
#     os.mkdir(SONGS_PATH)

# Spotify API credentials
client_credentials_manager = SpotifyClientCredentials(client_id=os.getenv("CLIENT_ID"),
                                                      client_secret=os.getenv("CLIENT_SECRET"))

# Initialize the Spotify client
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def analyzeUrl(playlist_url, songs_path,downloadbar: Progressbar):
    if "playlist" in playlist_url:
        process_playlist(playlist_url, songs_path, downloadbar)
    if "track" in playlist_url:
        process_singel_song(playlist_url, songs_path)


def searchsong(search_labelbox):

    results = sp.search(q=search_labelbox,type="track",limit=10)

    track_info = []

    for track in results["tracks"]["items"]:
        track_name = track["name"]
        artist_name = track['artists'][0]['name']
        track_url = track["external_urls"]["spotify"]

        track_info.append((track_name, artist_name, track_url))

    return track_info




def process_singel_song(song_url:str, song_path: str):

    song_id = song_url.split("/")[-1].split("?")[0]

    track = sp.track(song_id)

    song_name = track["name"]
    artist_name = track['artists'][0]['name']
    album_name = track['album']['name']
    album_art = track['album']['images'][0]['url']

    print(f"Song: {song_name}, Artist: {artist_name}, Album: {album_name}")
    print(f"Album Art URL: {album_art}")

    file_path = download_song(song_name,artist_name,song_path)

    add_metadata(file_path,song_name,artist_name,album_name,album_art)

    print(F"Download complete: {file_path}")




def process_playlist(playlist_url: str, songs_path: str, downloadbar: Progressbar):


     # Split the playlist URL string into a list of substrings
    playlist_id = playlist_url.split("/")[-1].split("?")[0]

        # Fetch the playlist data
    results = sp.playlist(playlist_id)

    total_songs = len(results["tracks"] ["items"])
    downloadbar["maximum"] = total_songs

    # Iterate over each track in the playlist and retrieve information
    for i , track in enumerate(results["tracks"] ["items"]):
        song_name = track['track']['name']
        artist_name = track['track']['artists'][0]['name']
        album_name = track['track']['album']['name']
        album_art = track['track']['album']['images'][0]['url']

        # Print track information
        print(f"Song: {song_name}, Artist: {artist_name}, Album: {album_name}")
        print(f"Album Art URL: {album_art}")



        # Download the song
        file_path = download_song(song_name, artist_name,songs_path)

        add_metadata(file_path, song_name, artist_name, album_name, album_art)

        downloadbar["value"] = i + 1
        downloadbar.update_idletasks()


def sanitize_filename(filename: str):
    # Remove characters that are not allowed in filenames
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def download_song(song_name: str, artist_name: str, songs_path:str):
    sanitized_song_name = sanitize_filename(song_name)


    # Check if the sanitized song name already ends with ".mp3"
    if not sanitized_song_name.endswith(".mp3"):
        file_name = path.join(songs_path, f"{sanitized_song_name}.mp3")
    else:
        file_name = path.join(songs_path, sanitized_song_name)

    # Print the file name to ensure it's correct
    print(f"Attempting to download: {song_name} by {artist_name}")
    print(f"Saving as: {file_name}")

    # Create a search query
    search_query = f"{song_name} {artist_name}"
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': path.join(songs_path, f"{sanitized_song_name}"),  # Remove .mp3 here
        'quite': True,       # Enable verbose logging for debugging
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"ytsearch:{search_query}"])

    # Check if the file was successfully downloaded
    if path.exists(file_name):
        print(f"Download completed: {file_name}")
    else:
        print(f"Download failed or file not found: {file_name}")
    
    return file_name





def add_metadata(file_path: str, song_name: str, artist_name: str, album_name: str, album_art_url: str):
    try:
        #load the mp3 file
        audio = EasyID3(file_path)
    except error:
        audio = EasyID3()

    #add metadata
    audio["title"] = song_name
    audio["artist"] = artist_name
    audio["album"] = album_name

    #save the metadata to the file
    audio.save(file_path)

    #add album art
    audio = ID3(file_path)
    album_art = requests.get(album_art_url).content # download album art
    audio["APIC"] = APIC(
        encoding = 3, # 3 is for utf-8
        mime = "image/jpeg",
        type = 3,
        desc = "Cover",
        data = album_art
    )
    
    audio.save(file_path) # save audio file
