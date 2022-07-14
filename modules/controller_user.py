import random
from hashlib import sha256


class ControllerUser:
    @staticmethod
    def hash_password(password: str, salt: str = ""):
        return sha256((password + salt).encode("utf-8")).hexdigest()

    @staticmethod
    def generate_salt():
        chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
        result = ""

        for _ in range(8):
            result += random.choice(chars)

        return result
    