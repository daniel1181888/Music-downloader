import os.path
from os import path
import re  # For sanitizing filenames
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




def process_playlist(playlist_url: str, songs_path: str):


     # Split the playlist URL string into a list of substrings
    playlist_id = playlist_url.split("/")[-1].split("?")[0]

        # Fetch the playlist data
    results = sp.playlist(playlist_id)

    # Iterate over each track in the playlist and retrieve information
    for track in results['tracks']['items']:
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
        'verbose': True,       # Enable verbose logging for debugging
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
