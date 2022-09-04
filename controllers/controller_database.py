from __future__ import annotations

import logging
from typing import List

from loguru import logger

from models.artist import Artist
from models.playlist import Playlist
from models.song import Song
from models.token import Token
from models.user import User
from utils.common_utils import CommonUtils


class ControllerDatabase:
    @staticmethod
    def get_user_playlists(user: User) -> List[Playlist]:
        """
        Used for getting all the users' playlists
        :param user: the user, whose playlists to fetch
        :return: a list of playlists
        """
        result = []

        try:
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
        except Exception as e:
            logger.exception(e)

        return result

    @staticmethod
    def get_playlist_by_uuid(playlist_uuid: str) -> Playlist:
        """
        Used for getting a playlist using its uuid
        :param playlist_uuid: the uuid of the playlist
        :return: a playlist model
        """
        result = None

        try:
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
        except Exception as e:
            logger.exception(e)

        return result

    @staticmethod
    def add_song_to_playlist(playlist_id: int, song_id: int) -> bool:
        """
        Used for adding a song to a playlist
        :param playlist_id: the id of the playlist that will contain the song
        :param song_id: id of the song to be added
        :return: bool of weather or not the insertion was successful
        """
        result = False
        try:
            with CommonUtils.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO songs_in_playlists (song_id, playlist_id) "
                        "VALUES (%(song_id)s, %(playlist_id)s) ",
                        {"playlist_id": playlist_id, "song_id": song_id}
                    )
                    result = True
        except Exception as e:
            logger.exception(e)

        return result

    @staticmethod
    def get_playlist_id_by_uuid(playlist_uuid: str) -> int:
        """
        Used for getting the id of a playlist from the uuid
        :param playlist_uuid: the uuid of the playlist
        :return: returns the id as an integer
        """
        result = None

        try:
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
        except Exception as e:
            logger.exception(e)

        return result

    @staticmethod
    def insert_user(user: User) -> bool:
        """
        Used for creating a new user
        :param user: the user to insert
        :return: bool of weather or not the insert was successful
        """
        result = False
        try:
            with CommonUtils.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO USERS "
                        "(user_name, password_hash, password_salt) "
                        "values (%(user_name)s, %(hashed_password)s, %(password_salt)s) ",
                        user.to_dict()
                    )
                    result = True
        except Exception as e:
            logger.exception(e)

        return result

    @staticmethod
    def insert_song(song: Song) -> Song:
        """
        Used for creating a new user
        :param song: the song that needs to be inserted
        :return: Song
        """

        try:
            with CommonUtils.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO songs "
                        "(song_name, album) "
                        "values (%(song_name)s, %(album)s) "
                        "RETURNING song_id ",
                        song.to_dict()
                    )

                    song_id = cur.fetchone()[0]
        except Exception as e:
            logger.exception(e)

        return ControllerDatabase.get_song(song_id)

    @staticmethod
    def get_song(song_id: int) -> Song:
        """
        Used for getting a user with a certain id
        :param song_id: the id of the song
        :return: a User model
        """
        try:
            with CommonUtils.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT song_id, song_uuid, song_name, album, modified, created, is_deleted "
                        "FROM songs "
                        "WHERE song_id = %(song_id)s LIMIT 1",
                        {"song_id": song_id})
                    song_id, song_uuid, song_name, album, modified, created, is_deleted = cur.fetchone()

            result = Song(
                song_id=song_id,
                song_uuid=str(song_uuid),
                song_name=song_name,
                album=album,
                modified=modified,
                created=created,
                is_deleted=is_deleted,
            )
        except Exception as e:
            logger.exception(e)

        return result

    @staticmethod
    def insert_playlist(playlist: Playlist) -> bool:
        """
        Used for creating a playlist
        :param playlist: the playlist to insert
        :return: bool of weather or not the insertion was successful
        """

        result = False
        try:
            with CommonUtils.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO playlists "
                        "(playlist_name, owner_user_id) "
                        "values (%(playlist_name)s, %(owner_user_id)s) ",
                        playlist.to_dict()
                    )
                    result = True
        except Exception as e:
            logger.exception(e)

        return result

    @staticmethod
    def insert_token(token: Token) -> Token:
        """
        Used for creating a playlist
        :param token: the token to insert
        :return: bool of weather or not the insertion was successful
        """
        result = None

        try:
            with CommonUtils.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO tokens "
                        "(user_user_id) "
                        "values (%(user_user_id)s) "
                        "RETURNING token_id",
                        token.to_dict()
                    )
                    token_id = cur.fetchone()[0]
            result = ControllerDatabase.get_token(token_id)
        except Exception as e:
            logger.exception(e)

        return result

    @staticmethod
    def delete_playlist(playlist_id: int) -> bool:
        """
        Used for deleting a playlist
        :param playlist_id: the id of the playlist
        :return: bool of weather or not the deletion was successful
        """
        result = False
        try:
            with CommonUtils.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "UPDATE playlists "
                        "SET is_deleted = true "
                        "WHERE playlist_id = %(playlist_id)s ",
                        {"playlist_id": playlist_id}
                    )
                    result = True
        except Exception as e:
            logger.exception(e)

        return result

    @staticmethod
    def remove_song_from_playlist(playlist_id: int, song_id: int) -> bool:
        """
        Used for removing a song from a playlist
        :param playlist_id: the id of the playlist
        :param song_id: the id of the song
        :return:
        """
        result = False

        try:
            with CommonUtils.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "UPDATE songs_in_playlists "
                        "SET is_deleted = true "
                        "WHERE song_id = %(song_id)s and playlist_id = %(playlist_id)s ",
                        {"song_id": song_id, "playlist_id": playlist_id}
                    )
                result = True
        except Exception as e:
            logger.exception(e)

        return result

    @staticmethod
    def get_playlist_songs(playlist: Playlist) -> List[Song]:
        """
        Used for getting all the songs of a playlist
        :param playlist: the playlist
        :return: a list of songs
        """
        result = []

        try:
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
        except Exception as e:
            logger.exception(e)

        return result

    @staticmethod
    def get_songs(page_size: int = -1, page_offset: int = 0) -> List[Song]:
        """
        Used for getting all song in a certain range
        :param page_size: the amount of songs to get
        :param page_offset: the starting point from where to start fetching the songs
        :return: a list of songs
        """
        result = []

        page_size_str = ""
        if page_size != -1:
            page_size_str = f"LIMIT %(page_size)s "

        try:
            with CommonUtils.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT songs.song_id, song_uuid, song_name, album, modified, songs.created, songs.is_deleted "
                        "FROM songs "
                        "WHERE songs.is_deleted = false "
                        f"{page_size_str}"
                        "OFFSET %(page_offset)s ",
                        {
                            "page_offset": page_offset,
                            "page_size": page_size
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
        except Exception as e:
            logger.exception(e)
        return result

    @staticmethod
    def get_song_id_by_uuid(song_uuid: str) -> int:
        """
        Used for getting the id of a song from its uuid
        :param song_uuid: the uuid of the song
        :return: the id as an integer
        """
        result = None

        try:
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
        except Exception as e:
            logger.exception(e)

        return result

    @staticmethod
    def check_if_username_taken(name: str) -> bool:
        """
        Checks if a username is taken
        :param name: the username
        :return: True if the username is taken else False
        """
        result = True
        try:
            with CommonUtils.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT user_id FROM USERS WHERE user_name = %(name)s LIMIT 1", {"name": name})
                    result = bool(cur.fetchone())
        except Exception as e:
            logger.exception(e)
        return result

    @staticmethod
    def get_user(user_id: int) -> User:
        """
        Used for getting a user with a certain id
        :param user_id: the id of the user
        :return: a User model
        """
        result = None
        try:
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
                playlists=ControllerDatabase.get_user_playlists(User(user_id=user_id)),
                hashed_password=hashed_password,
                password_salt=password_salt,
                token=ControllerDatabase.get_user_token(User(user_id=user_id)),
                modified=modified,
                created=created,
                is_deleted=is_deleted,
            )
        except Exception as e:
            logger.exception(e)

        return result

    @staticmethod
    def get_song(song_id: int) -> Song:
        """
        Used for getting a user with a certain id
        :param song_id: the id of the song
        :return: a User model
        """
        result =None
        try:
            with CommonUtils.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT song_id, song_uuid, song_name, album, modified, created, is_deleted "
                        "FROM songs "
                        "WHERE song_id = %(song_id)s LIMIT 1",
                        {"song_id": song_id})
                    song_id, song_uuid, song_name, album, modified, created, is_deleted = cur.fetchone()

            result = Song(
                song_id=song_id,
                song_uuid=str(song_uuid),
                song_name=song_name,
                album=album,
                modified=modified,
                created=created,
                is_deleted=is_deleted,
            )
        except Exception as e:
            logger.exception(e)

        return result

    @staticmethod
    def get_user_token(user: User) -> Token:
        """
        Used for getting a user with a certain id
        :param user: the user whose token need to be retrieved
        :return: a User model
        """
        result = Token()

        try:
            with CommonUtils.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT token_id, token_uuid, user_user_id, created, modified, is_deleted "
                        "FROM tokens "
                        "WHERE user_user_id = %(user_id)s AND is_deleted = false LIMIT 1",
                        {"user_id": user.user_id})
                    if cur.rowcount:
                        token_id, token_uuid, user_user_id, created, modified, is_deleted = cur.fetchone()

                        result = Token(
                            token_id=token_id,
                            token_uuid=str(token_uuid),
                            user_user_id=user_user_id,
                            modified=modified,
                            created=created,
                            is_deleted=is_deleted,
                        )
        except Exception as e:
            logger.exception(e)

        return result

    @staticmethod
    def get_token(token_id: int) -> Token:
        """
        Used for getting a user with a certain id
        :param token_id: the id of the token
        :return: a Token model
        """
        result = Token()

        try:
            with CommonUtils.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT token_id, token_uuid, user_user_id, created, modified, is_deleted "
                        "FROM tokens "
                        "WHERE (token_id = %(token_id)s AND is_deleted = false) LIMIT 1",
                        {"token_id": token_id}
                    )

                    if cur.rowcount:
                        token_id, token_uuid, user_user_id, created, modified, is_deleted = cur.fetchone()

                        result = Token(
                            token_id=token_id,
                            token_uuid=str(token_uuid),
                            user_user_id=user_user_id,
                            modified=modified,
                            created=created,
                            is_deleted=is_deleted,
                        )
        except Exception as e:
            logger.exception(e)

        return result

    @staticmethod
    def get_token_by_uuid(token_uuid: str) -> Token:
        """
        Used for getting a user with a certain id
        :param token_uuid: the uuid of the token
        :return: a Token model
        """
        result = Token()

        try:
            with CommonUtils.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT token_id, token_uuid, user_user_id, created, modified, is_deleted "
                        "FROM tokens "
                        "WHERE (token_uuid = %(token_uuid)s AND is_deleted = false) LIMIT 1",
                        {"token_uuid": token_uuid}
                    )

                    if cur.rowcount:
                        token_id, token_uuid, user_user_id, created, modified, is_deleted = cur.fetchone()

                        result = Token(
                            token_id=token_id,
                            token_uuid=str(token_uuid),
                            user_user_id=user_user_id,
                            modified=modified,
                            created=created,
                            is_deleted=is_deleted,
                        )
        except Exception as e:
            logger.exception(e)

        return result

    @staticmethod
    def delete_token(token: Token) -> bool:
        """
        Used for deleting a playlist
        :param token: the token to be deleted
        :return: bool of weather or not the deletion was successful
        """
        result = False

        try:
            with CommonUtils.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "UPDATE tokens "
                        "SET is_deleted = true "
                        "WHERE (token_id = %(token_id)s AND is_deleted = false) ",
                        token.to_dict()
                    )
                    result = True
        except Exception as e:
            logger.exception(e)

        return result

    @staticmethod
    def get_user_by_name(name: str) -> User:
        """
        Used for getting the user with a certain name
        :param name: the name of the user
        :return: a User model
        """
        result = None

        try:
            with CommonUtils.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT user_id, user_uuid, user_name, password_hash, password_salt, modified, created, is_deleted "
                        "FROM users "
                        "WHERE user_name = %(name)s LIMIT 1",
                        {"name": name}
                    )

                    user_id, user_uuid, name, hashed_password, password_salt, modified, created, is_deleted = cur.fetchone()

            result = User(
                user_id=user_id,
                user_uuid=str(user_uuid),
                user_name=name,
                playlists=ControllerDatabase.get_user_playlists(User(user_id=user_id)),
                hashed_password=hashed_password,
                password_salt=password_salt,
                token=ControllerDatabase.get_user_token(User(user_id=user_id)),
                modified=modified,
                created=created,
                is_deleted=is_deleted,
            )
        except Exception as e:
            logger.exception(e)

        return result

    @staticmethod
    def get_user_by_uuid(user_uuid: str) -> User:
        """
        Used for getting the user with a certain name
        :param user_uuid: the uuid of the user
        :return: a User model
        """
        result = None

        try:
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
                token=ControllerDatabase.get_user_token(User(user_id=user_id)),
                modified=modified,
                created=created,
                is_deleted=is_deleted,
            )
        except Exception as e:
            logger.exception(e)

        return result

    @staticmethod
    def get_user_id_by_name(name: str) -> int:
        """
        Used for getting a users' id from the uuid
        :param name: the users name
        :return: the users id
        """
        result = None
        try:
            with CommonUtils.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT user_id "
                                "FROM users "
                                "WHERE user_name = %(name)s LIMIT 1",
                                {"name": name})
                    fetch_result = cur.fetchone()

            if fetch_result:
                result = result[0]
        except Exception as e:
            logger.exception(e)

        return result

    @staticmethod
    def get_user_id_by_uuid(user_uuid: str) -> int:
        """
        Used for getting a users' id from the uuid
        :param user_uuid: the users uuid
        :return: the users id
        """
        result = None
        try:
            with CommonUtils.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT user_id "
                                "FROM users "
                                "WHERE user_uuid = %(user_uuid)s LIMIT 1",
                                {"user_uuid": user_uuid})
                    fetch_result = cur.fetchone()

            if fetch_result:
                result = result[0]
        except Exception as e:
            logger.exception(e)

        return result

    @staticmethod
    def add_subartist(parent_artist_id: int, child_artist_id: int) -> bool:
        """
        Used for getting a users' id from the uuid
        :param parent_artist_id: the id of the parent artist
        :param child_artist_id: the id of the child artist
        :return: the users id
        """
        result = False
        try:
            with CommonUtils.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO subartists_in_artists "
                        "(parent_artist_id, child_artist_id) "
                        "VALUES (%(parent_artist_id)s, %(child_artist_id)s) ",
                        {
                            "parent_artist_id": parent_artist_id,
                            "child_artist_id": child_artist_id
                        }
                    )
                    result = True
        except Exception as e:
            logger.exception(e)

        return result

    @staticmethod
    def remove_subartist(parent_artist_id: int, child_artist_id: int) -> bool:
        """
        Used for getting a users' id from the uuid
        :param parent_artist_id: the id of the parent artist
        :param child_artist_id: the id of the child artist
        :return: the users id
        """
        result = False
        try:
            with CommonUtils.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "UPDATE subartists_in_artists "
                        "set is_deleted = true "
                        "WHERE  parent_artist_id = %(parent_artist_id)s "
                        "AND child_artist_id = %(child_artist_id)s) ",
                        {
                            "parent_artist_id": parent_artist_id,
                            "child_artist_id": child_artist_id
                        }
                    )
                    result = True
        except Exception as e:
            logger.exception(e)

        return result

    @staticmethod
    def get_artists(page_size: int = -1, page_offset: int = 0) -> List[Artist]:
        """
        Used for getting all song in a certain range
        :param page_size: the amount of songs to get
        :param page_offset: the starting point from where to start fetching the songs
        :return: a list of songs
        """
        result = []

        page_size_str = ""
        if page_size != -1:
            page_size_str = f"LIMIT %(page_size)s "

        try:
            with CommonUtils.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT artist_id, artist_uuid, artist_name, created, modified, is_deleted "
                        "FROM artists "
                        "WHERE is_deleted = false "
                        f"{page_size_str}"
                        "OFFSET %(page_offset)s ",
                        {
                            "page_offset": page_offset,
                            "page_size": page_size
                        }
                    )
                    artists = cur.fetchall()

                    if artists:
                        for artist_id, artist_uuid, artist_name, created, modified, is_deleted in artists:
                            new_artist = Artist(
                                artist_id=artist_id,
                                artist_uuid=str(artist_uuid),
                                artist_name=artist_name,
                                child_artists_names=ControllerDatabase.get_artist_subartist_names(
                                    Artist(artist_id=artist_id)),
                                parent_artists_names=ControllerDatabase.get_artist_parent_artist_names(
                                    Artist(artist_id=artist_id)
                                ),
                                modified=modified,
                                created=created,
                                is_deleted=is_deleted,
                            )
                            result.append(new_artist)
        except Exception as e:
            logger.exception(e)
        return result

    @staticmethod
    def get_artist(artist_id: int) -> Artist:
        """
        Used for getting a user with a certain id
        :param artist_id: the id of the artist
        :return: a User model
        """
        result = None
        try:
            with CommonUtils.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT artist_id, artist_uuid, artist_name, modified, created, is_deleted "
                        "FROM artists "
                        "WHERE artist_id = %(artist_id)s LIMIT 1",
                        {"artist_id": artist_id})
                    artist_id, artist_uuid, artist_name, modified, created, is_deleted = cur.fetchone()

            result = Artist(
                artist_id=artist_id,
                artist_uuid=str(artist_uuid),
                artist_name=artist_name,
                child_artists_names=ControllerDatabase.get_artist_subartist_names(Artist(artist_id=artist_id)),
                parent_artists_names=ControllerDatabase.get_artist_parent_artist_names(
                    Artist(artist_id=artist_id)
                ),
                modified=modified,
                created=created,
                is_deleted=is_deleted,
            )
        except Exception as e:
            logger.exception(e)

        return result

    @staticmethod
    def get_artist_by_name(artist_name: str) -> Artist:
        """
        Used for getting a user with a certain id
        :param artist_name: the name of the artist
        :return: a User model
        """
        result = None
        try:
            with CommonUtils.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT artist_id, artist_uuid, artist_name, modified, created, is_deleted "
                        "FROM artists "
                        "WHERE artist_name = %(artist_name)s LIMIT 1",
                        {"artist_name": artist_name})

                    if cur.rowcount:
                        artist_id, artist_uuid, artist_name, modified, created, is_deleted = cur.fetchone()

                        result = Artist(
                            artist_id=artist_id,
                            artist_uuid=str(artist_uuid),
                            artist_name=artist_name,
                            child_artists_names=ControllerDatabase.get_artist_subartist_names(
                                Artist(artist_id=artist_id)
                            ),
                            parent_artists_names=ControllerDatabase.get_artist_parent_artist_names(
                                Artist(artist_id=artist_id)
                            ),
                            modified=modified,
                            created=created,
                            is_deleted=is_deleted,
                        )
        except Exception as e:
            logger.exception(e)

        return result

    @staticmethod
    def insert_artist(artist: Artist, parent_artist: Artist = None) -> bool:
        """
        Used for creating a new user
        :param artist: the artist to insert
        :param parent_artist: the parent artist of the inserted artist
        :return: bool of weather or not the insert was successful
        """
        result = False
        try:
            with CommonUtils.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO artists "
                        "(artist_name) "
                        "values (%(artist_name)s) "
                        "RETURNING artist_id ",
                        artist.to_dict()
                    )

                    artist_id = cur.fetchone()[0]

                    if parent_artist:
                        cur.execute(
                            "INSERT INTO subartists_in_artists "
                            "(child_artist_id, parent_artist_id) "
                            "values (%(child_artist_id)s, %(parent_artist_id)s) ",
                            {
                                "child_artist_id": artist_id,
                                "parent_artist_id": parent_artist.artist_id,
                            }
                        )
                    result = True
        except Exception as e:
            logger.exception(e)

        return result

    @staticmethod
    def get_artist_subartist_names(artist: Artist) -> list[str]:
        """
        Used for getting the subartists of a certain artist
        :param artist: the artist whose subartists need to be fetched
        :return: a list of artist names
        """
        result = []
        try:
            with CommonUtils.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT artists.artist_name "
                        "FROM artists "
                        "INNER JOIN subartists_in_artists as sia "
                        "ON sia.child_artist_id = artists.artist_id "
                        "WHERE sia.parent_artist_id = %(artist_id)s "
                        "AND sia.is_deleted = false "
                        "AND artists.is_deleted = false ",
                        {"artist_id": artist.artist_id}
                    )

                    if cur.rowcount:
                        result = [artist[0] for artist in cur.fetchall()]
        except Exception as e:
            logger.exception(e)

        return result

    @staticmethod
    def get_artist_parent_artist_names(artist: Artist) -> list[str]:
        """
        Used for getting the parent-artist of a certain artist
        :param artist: the artist whose parent-artists need to be fetched
        :return: a list of artist names
        """
        result = []
        try:
            with CommonUtils.connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT artists.artist_name "
                        "FROM artists "
                        "INNER JOIN subartists_in_artists as sia "
                        "ON sia.parent_artist_id = artists.artist_id "
                        "WHERE sia.child_artist_id = %(artist_id)s "
                        "AND sia.is_deleted = false "
                        "AND artists.is_deleted = false ",
                        {"artist_id": artist.artist_id})

                    if cur.rowcount:
                        result = [artist[0] for artist in cur.fetchall()]
        except Exception as e:
            logger.exception(e)

        return result
