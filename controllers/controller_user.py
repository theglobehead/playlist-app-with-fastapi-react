from __future__ import annotations

import os.path
from hashlib import sha256
from io import BytesIO

import numpy as np
from flask import send_file, Response

from controllers.controller_playlist import ControllerPlaylist
from models.user import User
from controllers.constants import PROFILE_PICTURE_PATH, DEFAULT_PROFILE_PICTURE_PATH
from utils.common_utils import CommonUtils


class ControllerUser:
    @staticmethod
    def hash_password(password: str, salt: str = "") -> str:
        """
        Used for hashing a users' password.
        Uses sha256
        :param password: the users passwords
        :param salt: the users' password salt
        :return: returns the hashed password
        """
        password_utf8 = (password + salt).encode("utf-8")
        password_hash = sha256(password_utf8)
        result = password_hash.hexdigest()

        return result

    @staticmethod
    def generate_salt() -> str:
        """
        Generates salt for the users' hashed password
        :return: an 8 character long string
        """
        chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
        random_chars = np.random.choice(list(chars), 8)
        result = "".join(random_chars)

        return result

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
                cur.execute("SELECT user_id, user_uuid, user_name, password_hash, password_salt, modified, created, is_deleted "
                            "FROM users "
                            "WHERE user_id = %(user_id)s LIMIT 1",
                            {"user_id": user_id})
                user_id, user_uuid, user_name, hashed_password, password_salt, modified, created, is_deleted = cur.fetchone()

        result = User(
            id=user_id,
            uuid=str(user_uuid),
            name=user_name,
            playlists=ControllerPlaylist.get_user_playlists(user_id),
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
                cur.execute("SELECT user_id, user_uuid, user_name, password_hash, password_salt, modified, created, is_deleted "
                            "FROM users "
                            "WHERE user_name = %(name)s LIMIT 1",
                            {"name": name})
                user_id, user_uuid, name, hashed_password, password_salt, modified, created, is_deleted = cur.fetchone()

        result = User(
            id=user_id,
            uuid=str(user_uuid),
            name=name,
            playlists=ControllerPlaylist.get_user_playlists(user_id),
            hashed_password=hashed_password,
            password_salt=password_salt,
            modified=modified,
            created=created,
            is_deleted=is_deleted,
        )

        return result

    @staticmethod
    def get_id_by_name(name: str) -> int:
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
    def get_id_by_uuid(user_uuid: str) -> int:
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
                if ControllerUser.check_if_username_taken(name):
                    cur.execute(
                        "SELECT user_id, user_uuid, user_name, password_hash, password_salt, modified, created, is_deleted "
                        "FROM users "
                        "WHERE user_name = %(name)s LIMIT 1",
                        {"name": name})
                    user_id, user_uuid, name, hashed_password, password_salt, modified, created, is_deleted = cur.fetchone()

                    if hashed_password == ControllerUser.hash_password(password, password_salt):
                        result = User(
                            id=user_id,
                            uuid=str(user_uuid),
                            name=name,
                            playlists=ControllerPlaylist.get_user_playlists(user_id),
                            hashed_password=hashed_password,
                            password_salt=password_salt,
                            modified=modified,
                            created=created,
                            is_deleted=is_deleted,
                        )
        return result

    @staticmethod
    def get_profile_pic(user_uuid: str) -> Response:
        """
        Used for getting a users profile pic
        :param user_uuid: uuid of the user
        :return: returns the file as a response
        """
        result = ""

        user_pic_path = f"{PROFILE_PICTURE_PATH}{user_uuid}.png"
        if os.path.exists(user_pic_path):
            result = user_pic_path
        else:
            result = DEFAULT_PROFILE_PICTURE_PATH

        with open(result, "rb") as f:
            result = BytesIO(f.read())

        return send_file(result, mimetype="image/jpeg")
