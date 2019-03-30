import plyvel
from ..config import Config

class Store:
    def name(): raise ("not implemented")

    def __init__(self, name):
        self.db = plyvel.DB(Config.get('data_dir') + '/' + Store.name(), create_if_missing=True)

    def close(self):
        return self.db.close()

    def _put(self, key, value):
        self.db.put(key, value)

    def _get(self, key):
        self.db.get(key)

    def _delete(self, key):
        self.db.delete(key)

    def _iter(self, start = None, stop = None):
        if not start or not stop:
            return self.db
        return self.db.iterator(start, stop)

    