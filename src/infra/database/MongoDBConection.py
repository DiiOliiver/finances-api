from contextlib import contextmanager

from pymongo import MongoClient


class MongoDBConnection:
    def __init__(self, uri: str):
        self.uri = uri
        self.conn = None

    @contextmanager
    def connection(self):
        self.conn = MongoClient(self.uri)
        try:
            yield self.conn
        finally:
            self.conn.close()

    def get_database(self):
        return self.db
