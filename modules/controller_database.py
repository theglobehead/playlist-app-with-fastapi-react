import datetime
from uuid import uuid4

from models.playlist import Playlist
from models.song import Song
from models.user import User
from modules.base_module import BaseModule
from modules.controller_user import ControllerUser


class ControllerDatabase:
    # Adding functions
    @staticmethod
    def insert_user(name: str, password: str):
        con = BaseModule.connection()
        cur = con.cursor()

        salt = ControllerUser.generate_salt()
        hashed_password = ControllerUser.hash_password(password=password, salt=salt)

        user = User(
            uuid=str(uuid4()),
            name=name,
            hashed_password=hashed_password,
            password_salt = salt
        )

        cur.execute(
            "INSERT INTO USERS "
            "(id, uuid, name, password_hash, password_salt, created, modified, is_deleted) "
            "values (%(id)s, %(uuid)s, %(name)s, %(hashed_password)s, %(password_salt)s, %(created)s, %(modified)s, %(is_deleted)s) ",
            user.to_dict()
        )
        con.commit()
        cur.close()


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