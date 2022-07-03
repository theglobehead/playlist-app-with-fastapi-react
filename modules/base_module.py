import psycopg2
from psycopg2.extensions import connection
from utils.logging_utils import LoggingUtils
from os import environ

class BaseModule:
    def __init__(self):
        pass

    @staticmethod
    def connection() -> connection:
        conn = None
        try:
            conn = psycopg2.connect(
                dbname=environ["DB_NAME"],
                user=environ["DB_USER"],
                host=environ["DB_HOST"],
                password=environ["DB_PASSWORD"],
                port=environ["DB_PORT"],
            )
        except Exception as e:
            LoggingUtils.log(e)
        return conn