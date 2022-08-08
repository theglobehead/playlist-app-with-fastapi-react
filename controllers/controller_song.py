import os

from werkzeug.datastructures import FileStorage

from controllers.constants import SONG_PATH, SONG_AUDIO_FILE_TYPE, SONG_PICTURE_PATH, SONG_IMAGE_FILE_TYPE
from models.song import Song


class ControllerSong:
    @staticmethod
    def upload_song(name: str, album: str, audio: FileStorage, image: FileStorage = None):
        song = Song(
            song_name=name,
            album=album,
        )

        from controllers.controller_database import ControllerDatabase
        song = ControllerDatabase.insert_song(song)

        audio.save(os.path.join(SONG_PATH, f"{ song.song_uuid }{ SONG_AUDIO_FILE_TYPE }"))

        if image:
            image.save(os.path.join(SONG_PICTURE_PATH, f"{ song.song_uuid }{ SONG_IMAGE_FILE_TYPE }"))

        return song