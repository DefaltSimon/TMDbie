# coding=utf-8
"""
Cache manager for TMDbie
"""
import logging
import time

from .abstract import TMDbType

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class CacheManager(metaclass=Singleton):
    def __init__(self, max_age=21600):  # 3 hours
        self.cache = {}

        self.name_to_id = {}
        self.id_to_timestamp = {}

        self.max_cache_age = int(max_age)

    def _is_valid(self, id_):
        if self.id_to_timestamp.get(id_):
            return (time.time() - self.id_to_timestamp[id_]) < self.max_cache_age
        else:
            return False

    def get_item_by_name(self, name):
        """
        Finds item by name, returns None if not found
        """
        query = str(name).lower()
        id_ = self.name_to_id.get(query)

        if self._is_valid(id_):
            return self.cache.get(id_)
        else:
            return None

    def get_item_by_id(self, id_):
        """
        Finds item by id, returns None if not found
        """
        if self._is_valid(id_):
            return self.cache.get(id_)
        else:
            return None

    def get_from_cache(self, search):
        if search is None:
            return None

        # Check if search is an id or a name
        try:
            int(search)
        except ValueError:
            return self.get_item_by_name(search)
        else:
            return self.get_item_by_id(search)

    def item_set(self, item):
        if not isinstance(item, TMDbType):
            raise ValueError("invalid item type: {}".format(type(item)))

        self.cache[item.id] = item
        self.name_to_id[str(item.title.lower())] = item.id
        self.id_to_timestamp[item.id] = time.time()

        log.info("Added new {} to cache".format(type(item).__name__))
