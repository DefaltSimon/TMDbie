"""
Cache manager for TMDbie
"""
import logging
from .utils import Singleton
from ._types import TVShow, Movie, Person

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

class CacheManager(metaclass=Singleton):
    def __init__(self, max_age=21600): # 3 hours
        self.people = {}
        self.movies = {}
        self.tv = {}

        self.nametoid = {}

        self.max_cache_age = int(max_age)

    def get_from_cache(self, id_=None, name=None, type_=None):
        assert id_ or name

        if id_:
            if not type_:
                people_s = self.people.get(id_)
                if people_s: return people_s

                movie_s = self.movies.get(id_)
                if movie_s: return movie_s

                tv_s = self.tv.get(id_)
                return tv_s

            else:
                if type_ == "people":
                    return self.people.get(id_)
                elif type_ == "movies":
                    return self.movies.get(id_)
                elif type_ == "tv":
                    return self.tv.get(id_)
                else:
                    raise ValueError("invalid type_: {}".format(type_))

        elif name:
            query = str(name).lower()

            id_ = self.nametoid.get(query)

            # Blind search
            people_s = self.people.get(id_)
            if people_s: return people_s

            movie_s = self.movies.get(id_)
            if movie_s: return movie_s

            tv_s = self.tv.get(id_)
            return tv_s

    def item_set(self, item):
        if isinstance(item, Movie):
            self.movies[item.id] = item
            self.nametoid[str(item.title.lower())] = item.id

            log.info("Added new movie to cache")

        elif isinstance(item, TVShow):
            self.tv[item.id] = item
            self.nametoid[str(item.name.lower())] = item.id

            log.info("Added new tv show to cache")

        elif isinstance(item, Person):
            self.people[item.id] = item
            self.nametoid[str(item.name.lower())] = item.id

            log.info("Added new person to cache")

        else:
            raise ValueError("invalid item type: {}".format(type(item)))