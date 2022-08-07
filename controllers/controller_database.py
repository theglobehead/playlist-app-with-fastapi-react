from __future__ import annotations

import os
from typing import List

from flask import Response, send_file
from six import BytesIO

from controllers.constants import PROFILE_PICTURE_PATH, DEFAULT_PROFILE_PICTURE_PATH, SONG_PICTURE_PATH
from models.playlist import Playlist
from models.song import Song
from models.user import User
from utils.common_utils import CommonUtils
from controllers.controller_user import ControllerUser


class ControllerDatabase:
    @staticmethod
    def get_user_playlists(user: User) -> List[Playlist]:
        """
        Used for getting all the users' playlists
        :param user: the user, whose playlists to fetch
        :return: a list of playlists
        """
        result = []

        with CommonUtils.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT playlist_id, playlist_name, playlist_uuid, modified, created, is_deleted "
                    "FROM playlists "
                    "WHERE owner_user_id = %(user_id)s and is_deleted = false ",
                    user.to_dict()
                )
                playlists = cur.fetchall()

                if playlists:
                    for playlist_id, playlist_name, playlist_uuid, modified, created, is_deleted in playlists:
                        playlist_songs = ControllerDatabase.get_playlist_songs(Playlist(playlist_id=playlist_id))
                        new_playlist = Playlist(
                            playlist_id=playlist_id,
                            playlist_uuid=str(playlist_uuid),
                            playlist_name=playlist_name,
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
                    playlist_songs = ControllerDatabase.get_playlist_songs(Playlist(playlist_id=playlist_id))
                    result = Playlist(
                        playlist_id=playlist_id,
                        playlist_uuid=str(playlist_uuid),
                        playlist_name=playlist_name,
                        songs=playlist_songs,
                        modified=modified,
                        created=created,
                        is_deleted=is_deleted,
                    )
        return result

    @staticmethod
    def add_song_to_playlist(playlist_id: int, song_id: int) -> None:
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
        :param playlist_uuid: the uuid of the playlist
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
            user_name=name,
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
        print(playlist_name)
        print(type(playlist_name))
        print(owner_id)
        playlist = Playlist(
            playlist_name=playlist_name,
            owner_user_id=owner_id
        )

        with CommonUtils.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO playlists "
                    "(playlist_name, owner_user_id) "
                    "values (%(playlist_name)s, %(owner_user_id)s) ",
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

    @staticmethod
    def get_playlist_songs(playlist: Playlist) -> List[Song]:
        """
        Used for getting all the songs of a playlist
        :param playlist: the playlist
        :return: a list of songs
        """
        result = []

        with CommonUtils.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT songs.song_id, song_uuid, song_name, album, modified, songs.created, songs.is_deleted "
                    "FROM songs "
                    "INNER JOIN songs_in_playlists sip on songs.song_id = sip.song_id AND sip.playlist_id = %(playlist_id)s "
                    "WHERE songs.is_deleted = false and sip.is_deleted = false",
                    playlist.to_dict()
                )
                playlists = cur.fetchall()

                if playlists:
                    for song_id, song_uuid, song_name, album, modified, created, is_deleted in playlists:
                        new_song = Song(
                            song_id=song_id,
                            song_uuid=str(song_uuid),
                            song_name=song_name,
                            album=album,
                            modified=modified,
                            created=created,
                            is_deleted=is_deleted,
                        )
                        result.append(new_song)
        return result

    @staticmethod
    def get_songs(amount: int = -1, starting_from: int = 0) -> List[Song]:
        """
        Used for getting all song in a certain range
        :param amount: the amount of songs to get
        :param starting_from: the starting point from where to start fetching the songs
        :return: a list of songs
        """
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
                            song_id=song_id,
                            song_uuid=str(song_uuid),
                            song_name=song_name,
                            album=album,
                            modified=modified,
                            created=created,
                            is_deleted=is_deleted,
                        )
                        result.append(new_song)
        return result

    @staticmethod
    def get_song_id_by_uuid(song_uuid: str) -> int:
        """
        Used for getting the id of a song from its uuid
        :param song_uuid: the uuid of the song
        :return: the id as an integer
        """
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
    def get_song_pic(song_uuid: str) -> Response:
        """
        Returns the songs picture
        :param song_uuid: the uuid of the song
        :return: returns the image as a flask response
        """
        result = None

        song_pic_path = f"{SONG_PICTURE_PATH}{song_uuid}.jpg"
        if os.path.exists(song_pic_path):
            result = song_pic_path
        else:
            result = DEFAULT_PROFILE_PICTURE_PATH

        with open(result, "rb") as f:
            result = BytesIO(f.read())

        return send_file(result, mimetype="image/jpeg")

    @staticmethod
    def check_if_username_taken(name: str) -> bool:
        """
        Checks if a username is taken
        :param name: the username
        :return: True if the username is taken else False
        """
        with CommonUtils.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT user_id FROM USERS WHERE user_name = %(name)s LIMIT 1", {"name": name})
                result = bool(cur.fetchone())
        return result

    @staticmethod
    def get_user(user_id: int) -> User:
        """
        Used for getting a user with a certain id
        :param user_id: the id of the user
        :return: a User model
        """
        with CommonUtils.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT user_id, user_uuid, user_name, password_hash, password_salt, modified, created, is_deleted "
                    "FROM users "
                    "WHERE user_id = %(user_id)s LIMIT 1",
                    {"user_id": user_id})
                user_id, user_uuid, user_name, hashed_password, password_salt, modified, created, is_deleted = cur.fetchone()

        result = User(
            user_id=user_id,
            user_uuid=str(user_uuid),
            user_name=user_name,
            playlists=ControllerDatabase.get_user_playlists(user_id),
            hashed_password=hashed_password,
            password_salt=password_salt,
            modified=modified,
            created=created,
            is_deleted=is_deleted,
        )

        return result

    @staticmethod
    def get_user_by_name(name: str) -> User:
        """
        Used for getting the user with a certain name
        :param name: the name of the user
        :return: a User model
        """
        with CommonUtils.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT user_id, user_uuid, user_name, password_hash, password_salt, modified, created, is_deleted "
                    "FROM users "
                    "WHERE user_name = %(name)s LIMIT 1",
                    {"name": name})
                user_id, user_uuid, name, hashed_password, password_salt, modified, created, is_deleted = cur.fetchone()

        result = User(
            user_id=user_id,
            user_uuid=str(user_uuid),
            user_name=name,
            playlists=ControllerDatabase.get_user_playlists(user_id),
            hashed_password=hashed_password,
            password_salt=password_salt,
            modified=modified,
            created=created,
            is_deleted=is_deleted,
        )

        return result

    @staticmethod
    def get_user_by_uuid(user_uuid: str) -> User:
        """
        Used for getting the user with a certain name
        :param user_uuid: the uuid of the user
        :return: a User model
        """
        with CommonUtils.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT user_id, user_uuid, user_name, password_hash, password_salt, modified, created, is_deleted "
                    "FROM users "
                    "WHERE user_uuid = %(user_uuid)s LIMIT 1",
                    {"user_uuid": user_uuid})
                user_id, user_uuid, name, hashed_password, password_salt, modified, created, is_deleted = cur.fetchone()

        result = User(
            user_id=user_id,
            user_uuid=str(user_uuid),
            user_name=name,
            playlists=ControllerDatabase.get_user_playlists(User(user_id=user_id)),
            hashed_password=hashed_password,
            password_salt=password_salt,
            modified=modified,
            created=created,
            is_deleted=is_deleted,
        )

        return result

    @staticmethod
    def get_user_id_by_name(name: str) -> int:
        """
        Used for getting a users' id from the uuid
        :param name: the users name
        :return: the users id
        """
        with CommonUtils.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT user_id "
                            "FROM users "
                            "WHERE user_name = %(name)s LIMIT 1",
                            {"name": name})
                result = cur.fetchone()

        if result:
            result = result[0]

        return result

    @staticmethod
    def get_user_id_by_uuid(user_uuid: str) -> int:
        """
        Used for getting a users' id from the uuid
        :param user_uuid: the users uuid
        :return: the users id
        """
        with CommonUtils.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT user_id "
                            "FROM users "
                            "WHERE user_uuid = %(user_uuid)s LIMIT 1",
                            {"user_uuid": user_uuid})
                result = cur.fetchone()

        if result:
            result = result[0]

        return result

    @staticmethod
    def authenticate_user(name: str, password: str) -> User | None:
        """
        Used for checking if the user entered valid data, when logging in
        :param name: the name entered
        :param password: the password entered
        :return: Returns the User, if the form is valid, else it returns false
        """
        result = None

        with CommonUtils.connection() as conn:
            with conn.cursor() as cur:
                if ControllerDatabase.check_if_username_taken(name):
                    cur.execute(
                        "SELECT user_id, user_uuid, user_name, password_hash, password_salt, modified, created, is_deleted "
                        "FROM users "
                        "WHERE user_name = %(name)s LIMIT 1",
                        {"name": name})
                    user_id, user_uuid, name, hashed_password, password_salt, modified, created, is_deleted = cur.fetchone()

                    if hashed_password == ControllerUser.hash_password(password, password_salt):
                        result = User(
                            user_id=user_id,
                            user_uuid=str(user_uuid),
                            user_name=name,
                            playlists=ControllerDatabase.get_user_playlists(User(user_id=user_id)),
                            hashed_password=hashed_password,
                            password_salt=password_salt,
                            modified=modified,
                            created=created,
                            is_deleted=is_deleted,
                        )
        return result

    @staticmethod
    def get_user_profile_pic(user_uuid: str) -> Response:
        """
        Used for getting a users profile pic
        :param user_uuid: uuid of the user
        :return: returns the file as a response
        """
        result = ""

        print("user_uuid:", user_uuid)
        print("test")
        user_pic_path = f"{PROFILE_PICTURE_PATH}{user_uuid}.png"
        if os.path.exists(user_pic_path):
            print("path exists")
            result = user_pic_path
        else:
            print("it doesnt")
            result = DEFAULT_PROFILE_PICTURE_PATH

        with open(result, "rb") as f:
            print("open")
            result = BytesIO(f.read())

        return send_file(result, mimetype="image/png")
