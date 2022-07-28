from typing import List

from controllers.controller_song import ControllerSong
from models.playlist import Playlist
from utils.common_utils import CommonUtils


class ControllerPlaylist:
    @staticmethod
    def get_user_playlists(user_id: id) -> List[Playlist]:
        """
        Used for getting all the users' playlists
        :param user_id: the id of the user
        :return: a list of playlists
        """
        result = []

        with CommonUtils.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT playlist_id, playlist_name, playlist_uuid, modified, created, is_deleted "
                    "FROM playlists "
                    "WHERE owner_user_id = %(user_id)s and is_deleted = false ",
                    {"user_id": user_id}
                )
                playlists = cur.fetchall()

                if playlists:
                    for playlist_id, playlist_name, playlist_uuid, modified, created, is_deleted in playlists:
                        playlist_songs = ControllerSong.get_playlist_songs(playlist_id)
                        new_playlist = Playlist(
                            id=playlist_id,
                            uuid=str(playlist_uuid),
                            name=playlist_name,
                            songs=playlist_songs,
                            modified=modified,
                            created=created,
                            is_deleted=is_deleted,
                        )
                        result.append(new_playlist)
        return result

    @staticmethod
    def get_playlist_by_uuid(playlist_uuid: str) -> Playlist:
        """
        Used for getting a playlist using its uuid
        :param playlist_uuid: the uuid of the playlist
        :return: a playlist model
        """
        result = None

        with CommonUtils.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT playlist_id, playlist_name, playlist_uuid, modified, created, is_deleted "
                    "FROM playlists "
                    "WHERE playlist_uuid = %(playlist_uuid)s",
                    {"playlist_uuid": playlist_uuid}
                )
                result = cur.fetchone()

                if result:
                    playlist_id, playlist_name, playlist_uuid, modified, created, is_deleted = result
                    playlist_songs = ControllerSong.get_playlist_songs(playlist_id)
                    result = Playlist(
                        id=playlist_id,
                        uuid=str(playlist_uuid),
                        name=playlist_name,
                        songs=playlist_songs,
                        modified=modified,
                        created=created,
                        is_deleted=is_deleted,
                    )
        return result

    @staticmethod
    def add_song(playlist_id: int, song_id: int) -> None:
        """
        Used for adding a song to a playlist
        :param playlist_id: the id of the playlist that will contain the song
        :param song_id: id of the song to be added
        :return: None
        """
        with CommonUtils.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO songs_in_playlists (song_id, playlist_id) "
                    "VALUES (%(song_id)s, %(playlist_id)s) ",
                    {"playlist_id": playlist_id, "song_id": song_id}
                )

    @staticmethod
    def get_playlist_id_by_uuid(playlist_uuid: str) -> int:
        """
        Used for getting the id of a playlist from the uuid
        :param playlist_uuid: the uuid of the palylist
        :return: returns the id as an integer
        """
        result = None

        with CommonUtils.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT playlist_id "
                    "FROM playlists "
                    "WHERE playlist_uuid = %(playlist_uuid)s ",
                    {"playlist_uuid": playlist_uuid}
                )
                playlist_id = cur.fetchone()

                if playlist_id:
                    result = playlist_id[0]

        return result
