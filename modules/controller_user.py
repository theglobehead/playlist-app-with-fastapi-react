from hashlib import sha256

import numpy as np

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
        con = BaseModule.connection()
        cur = con.cursor()

        cur.execute("SELECT COUNT(id) FROM USERS WHERE name = %(name)s LIMIT 1", {"name": name})

        return bool(cur.fetchone()[0])