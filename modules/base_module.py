import psycopg2
from psycopg2.extensions import connection
from os import environ

class BaseModule:
    @staticmethod
    def connection() -> connection:
        conn = None
        #try:
        conn = psycopg2.connect(
            host=environ["DB_HOST"],
            database=environ["DB_NAME"],
            user=environ["DB_USER"],
            password=environ["DB_PASSWORD"],
        )
        #except Exception as e:
        #    LoggingUtils.log(e)
        return conn

#class Connection():
#    def __enter__(self: connection) -> connection:
#        return super().__enter__()
#
#    def __init__(self) -> None:
#        self = BaseModule.connection()
#
#    def __exit__(self: connection):
#        self.commit()
#
#class Cursor():
#    def __enter__(self: psycopg2.cursor) -> psycopg2.cursor:
#        return super().__enter__()
#
#    def __init__(self) -> None:
#        self = BaseModule.connection()
#
#    def __exit__(self: psycopg2.cursor):
#        self.close()