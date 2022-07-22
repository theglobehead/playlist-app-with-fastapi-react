import os.path
from hashlib import sha256
from io import BytesIO

import numpy as np
from flask import send_file

from models.user import User
from controllers.constants import PROFILE_PICTURE_PATH, DEFAULT_PROFILE_PICTURE_PATH
from utils.common_utils import CommonUtils


class ControllerUser:
    @staticmethod
    def hash_password(password: str, salt: str = "") -> str:
        password_utf8 = (password + salt).encode("utf-8")
        password_hash = sha256(password_utf8)
        result = password_hash.hexdigest()

        return result

    @staticmethod
    def generate_salt() -> str:
        chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
        random_chars = np.random.choice(list(chars), 8)
        result = "".join(random_chars)

        return result

    @staticmethod
    def check_if_username_taken(name: str) -> bool:
        with CommonUtils.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT user_id FROM USERS WHERE name = %(name)s LIMIT 1", {"name": name})
                result = bool(cur.fetchone())
        return result

    @staticmethod
    def get_user(user_id: int) -> User:
        with CommonUtils.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT user_id, uuid, name, password_hash, password_salt, modified, created, is_deleted "
                            "FROM users "
                            "WHERE user_id = %(user_id)s LIMIT 1",
                            {"user_id": user_id})
                user_id, uuid, name, hashed_password, password_salt, modified, created, is_deleted = cur.fetchone()

        result = User(
            user_id=user_id,
            uuid=uuid,
            name=name,
            hashed_password=hashed_password,
            password_salt=password_salt,
            modified=modified,
            created=created,
            is_deleted=is_deleted,
        )

        return result

    @staticmethod
    def get_user_by_name(name: str) -> User:
        with CommonUtils.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT user_id, uuid, name, password_hash, password_salt, modified, created, is_deleted "
                            "FROM users "
                            "WHERE name = %(name)s LIMIT 1",
                            {"name": name})
                user_id, uuid, name, hashed_password, password_salt, modified, created, is_deleted = cur.fetchone()

        result = User(
            user_id=user_id,
            uuid=uuid,
            name=name,
            hashed_password=hashed_password,
            password_salt=password_salt,
            modified=modified,
            created=created,
            is_deleted=is_deleted,
        )

        return result

    @staticmethod
    def get_id_by_name(name: str) -> int:
        with CommonUtils.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT user_id "
                            "FROM users "
                            "WHERE name = %(name)s LIMIT 1",
                            {"name": name})
                result = cur.fetchone()

        if result:
            result = result[0]

        return result

    @staticmethod
    def get_profile_pic(uuid: str) -> str:
        result = ""

        user_pic_path = f"{PROFILE_PICTURE_PATH}{uuid}.png"
        if os.path.exists(user_pic_path):
            result = user_pic_path
        else:
            result = DEFAULT_PROFILE_PICTURE_PATH

        with open(result, "rb") as f:
            result = BytesIO(f.read())

        return send_file(result, mimetype="image/jpeg")
