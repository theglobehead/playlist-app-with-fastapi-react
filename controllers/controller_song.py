import os
from io import BytesIO
from typing import List

from flask import send_file, Response

from controllers.constants import SONG_PICTURE_PATH, DEFAULT_PROFILE_PICTURE_PATH
from models.song import Song
from utils.common_utils import CommonUtils


class ControllerSong:
    @staticmethod
    def get_playlist_songs(playlist_id: int) -> List[Song]:
        result = []

        with CommonUtils.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT songs.song_id, song_uuid, song_name, album, modified, songs.created, songs.is_deleted "
                    "FROM songs "
                    "INNER JOIN songs_in_playlists sip on songs.song_id = sip.song_id AND sip.playlist_id = %(playlist_id)s "
                    "WHERE songs.is_deleted = false and sip.is_deleted = false",
                    {"playlist_id": playlist_id}
                )
                playlists = cur.fetchall()

                if playlists:
                    for song_id, song_uuid, song_name, album, modified, created, is_deleted in playlists:
                        new_song = Song(
                            id=song_id,
                            uuid=str(song_uuid),
                            name=song_name,
                            album=album,
                            modified=modified,
                            created=created,
                            is_deleted=is_deleted,
                        )
                        result.append(new_song)
        return result

    @staticmethod
    def get_songs(amount: int = -1, starting_from: int = 0):
        result = []

        amount_str = ""
        if amount != -1:
            amount_str = f"LIMIT %(amount)s "

        with CommonUtils.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT songs.song_id, song_uuid, song_name, album, modified, songs.created, songs.is_deleted "
                    "FROM songs "
                    "WHERE songs.is_deleted = false "
                    f"{amount_str}"
                    "OFFSET %(starting_from)s ",
                    {
                        "starting_from": starting_from,
                        "amount": amount
                    }
                )
                playlists = cur.fetchall()

                if playlists:
                    for song_id, song_uuid, song_name, album, modified, created, is_deleted in playlists:
                        new_song = Song(
                            id=song_id,
                            uuid=str(song_uuid),
                            name=song_name,
                            album=album,
                            modified=modified,
                            created=created,
                            is_deleted=is_deleted,
                        )
                        result.append(new_song)
        return result

    @staticmethod
    def get_song_id_by_uuid(song_uuid: str) -> int:
        result = None

        with CommonUtils.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT song_id "
                    "FROM songs "
                    "WHERE song_uuid = %(song_uuid)s AND is_deleted = false ",
                    {"song_uuid": song_uuid}
                )
                song_id = cur.fetchone()

                if song_id:
                    result = song_id[0]

        return result

    @staticmethod
    def get_song_pic(uuid: str) -> Response:
        result = None

        song_pic_path = f"{SONG_PICTURE_PATH}{uuid}.jpg"
        if os.path.exists(song_pic_path):
            result = song_pic_path
        else:
            result = DEFAULT_PROFILE_PICTURE_PATH

        with open(result, "rb") as f:
            result = BytesIO(f.read())

        return send_file(result, mimetype="image/jpeg")
