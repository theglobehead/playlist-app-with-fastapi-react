from __future__ import annotations

import os.path
from hashlib import sha256
from io import BytesIO
import numpy as np
from flask import send_file, Response

from controllers.controller_database import ControllerDatabase
from controllers.controller_playlist import ControllerPlaylist
from models.token import Token
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
    def create_user(name: str, password: str):
        salt = ControllerUser.generate_salt()
        hashed_password = ControllerUser.hash_password(password, salt)

        user = User(
            name=name,
            password_salt=salt,
            password=hashed_password,
        )

        return ControllerDatabase.insert_user(user)

    @staticmethod
    def log_user_in(name: str, password: str, remember_me: bool) -> User | None:
        """
        Used for checking if the user entered valid data, when logging in
        :param name: the name entered
        :param password: the password entered
        :param remember_me: weather or not to remember the user
        :return: Returns the User, if the form is valid, else it returns false
        """
        result = None

        username_taken = ControllerDatabase.check_if_username_taken(name)

        if username_taken:
            user = ControllerDatabase.get_user_by_name(name)
            hashed_password = ControllerUser.hash_password(password, user.password_salt)

            if user.hashed_password == hashed_password:
                if remember_me:
                    user.token = ControllerUser.create_token(user)

                result = user

        return result

    @staticmethod
    def create_token(user: User) -> Token:
        if user.token.token_id:
            ControllerDatabase.delete_token(user.token)

        new_token = ControllerDatabase.insert_token(Token(user_user_id=user.user_id))

        return new_token

    @staticmethod
    def validate_register_form(name: str, pass1: str, pass2: str):
        """
        Used for validating a register form.
        If the form is invalid, it flashes a message.
        :param name: the username entered
        :param pass1: the first password entered
        :param pass2: the second password entered
        :return: boolean of weather or not the form is valid
        """
        result = True

        if not all((pass1, pass2)):
            result = False
        elif not name:
            result = False
        elif len(name) > 64:
            result = False
        elif pass1 != pass2:
            result = False
        elif len(pass1) < 8:
            result = False
        elif ControllerDatabase.check_if_username_taken(name=name):
            result = False

        return result
