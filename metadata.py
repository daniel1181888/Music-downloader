import requests
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC



class MetadataManager:
    @staticmethod
    def add_metadata(file_path, song_name, artist_name, album_name, album_art_url):
        audio = EasyID3(file_path)
        audio['title'] = song_name
        audio['artist'] = artist_name
        audio['album'] = album_name
        audio.save()

        album_art = requests.get(album_art_url).content
        audio = ID3(file_path)
        audio['APIC'] = APIC(
            encoding=3,
            mime='image/jpeg',
            type=3,
            desc='Cover',
            data=album_art
        )
        audio.save()