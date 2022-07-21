import os.path
from hashlib import sha256

import flask
import numpy as np

from models.user import User
from modules.base_module import BaseModule


class ControllerUser:
    @staticmethod
    def hash_password(password: str, salt: str = "") -> str:
        return sha256((password + salt).encode("utf-8")).hexdigest()

    @staticmethod
    def generate_salt() -> str:
        chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
        return "".join(np.random.choice(list(chars), 8))

    @staticmethod
    def check_if_username_taken(name: str) -> bool:
        with BaseModule.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(user_id) FROM USERS WHERE name = %(name)s LIMIT 1", {"name": name})
                result = cur.fetchone()[0]
        return bool(result)

    @staticmethod
    def get_user(user_id: int) -> User:
        with BaseModule.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT user_id, uuid, name, password_hash, password_salt, modified, created, is_deleted "
                            "FROM users "
                            "WHERE user_id = %(user_id)s LIMIT 1",
                            {"user_id": user_id})
                result = cur.fetchone()

        if result:
            result = User(
                user_id=result[0],
                uuid=str(result[1]),
                name=result[2],
                hashed_password=result[3],
                password_salt=result[4],
                modified=result[5],
                created=result[6],
                is_deleted=result[7],
            )

        return result

    @staticmethod
    def get_id_by_name(name: str) -> int:
        with BaseModule.connection() as conn:
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

        path = "/static/images/profile_pictures/"
        if os.path.exists(f"../static/images/profile_pictures/{uuid}.png"):
            result = f"{path}{uuid}.png"
        else:
            result = f"{path}default.png"

        return result
