import psycopg2
from psycopg2.extensions import connection
from os import environ




class CommonUtils:
    @staticmethod
    def connection() -> connection:
        conn = None
        try:
            conn = psycopg2.connect(
                host=environ["DB_HOST"],
                database=environ["DB_NAME"],
                user=environ["DB_USER"],
                password=environ["DB_PASSWORD"],
            )
        except Exception as e:
            print(e) # logging placeholdere)
        return conn
