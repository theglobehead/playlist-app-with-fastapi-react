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
