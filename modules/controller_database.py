from models.playlist import Playlist
from models.song import Song
from models.user import User
from modules.base_module import BaseModule
from modules.controller_user import ControllerUser


class ControllerDatabase:
    # Adding functions
    @staticmethod
    def insert_user(name: str, password: str):
        salt = ControllerUser.generate_salt()
        hashed_password = ControllerUser.hash_password(password=password, salt=salt)

        user = User(
            name=name,
            hashed_password=hashed_password,
            password_salt=salt
        )

        with BaseModule.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO USERS "
                    "(name, password_hash, password_salt) "
                    "values (%(name)s, %(hashed_password)s, %(password_salt)s) ",
                    user.to_dict()
                )


    @staticmethod
    def insert_play_list(play_list: Playlist):
        pass

    @staticmethod
    def insert_song(song: Song):
        pass

    # Removing functions
    @staticmethod
    def remove_user(user: User):
        pass

    @staticmethod
    def remove_play_list(play_list: Playlist):
        pass

    @staticmethod
    def remove_song(song: Song):
        pass