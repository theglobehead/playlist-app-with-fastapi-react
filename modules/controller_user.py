import random
from hashlib import sha256

from modules.base_module import BaseModule


class ControllerUser:
    @staticmethod
    def hash_password(password: str, salt: str = "") -> str:
        return sha256((password + salt).encode("utf-8")).hexdigest()

    @staticmethod
    def generate_salt() -> str:
        chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
        result = ""

        for _ in range(8):
            result += random.choice(chars)

        return result

    @staticmethod
    def check_if_username_taken(name: str) -> bool:
        con = BaseModule.connection()
        cur = con.cursor()

        cur.execute("SELECT COUNT(id) FROM USERS WHERE name = %(name)s", {"name": name})

        if cur.fetchone()[0]:
            return False
        return True
    