from models.playlist import Playlist
from models.song import Song
from models.user import User
from utils.common_utils import CommonUtils
from controllers.controller_user import ControllerUser


class ControllerDatabase:
    # Adding functions
    @staticmethod
    def insert_user(name: str, password: str) -> None:
        """
        Used for creating a new user
        :param name: the name of the user
        :param password: the password of the user
        :return: None
        """
        salt = ControllerUser.generate_salt()
        hashed_password = ControllerUser.hash_password(password=password, salt=salt)

        user = User(
            name=name,
            hashed_password=hashed_password,
            password_salt=salt
        )

        with CommonUtils.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO USERS "
                    "(user_name, password_hash, password_salt) "
                    "values (%(name)s, %(hashed_password)s, %(password_salt)s) ",
                    user.to_dict()
                )

    @staticmethod
    def insert_playlist(playlist_name: str, owner_id: int):
        """
        Used for creating a playlist
        :param playlist_name: The name of the playlist
        :param owner_id: the id of the playlists' owner
        :return: 
        """
        playlist = Playlist(
            name=playlist_name,
            owner_user_id=owner_id
        )

        with CommonUtils.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO playlists "
                    "(playlist_name, owner_user_id) "
                    "values (%(name)s, %(owner_user_id)s) ",
                    playlist.to_dict()
                )

    @staticmethod
    def delete_playlist(playlist_id: int) -> None:
        """
        Used for deleting a playlist
        :param playlist_id: the id of the playlist
        :return: None
        """
        with CommonUtils.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE playlists "
                    "SET is_deleted = true "
                    "WHERE playlist_id = %(playlist_id)s ",
                    {"playlist_id": playlist_id}
                )

    @staticmethod
    def remove_song_from_playlist(playlist_id: int, song_id: int) -> None:
        """
        Used for removing a song from a playlist
        :param playlist_id: the id of the playlist
        :param song_id: the id of the song
        :return:
        """
        with CommonUtils.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE songs_in_playlists "
                    "SET is_deleted = true "
                    "WHERE song_id = %(song_id)s and playlist_id = %(playlist_id)s ",
                    {"song_id": song_id, "playlist_id": playlist_id}
                )
