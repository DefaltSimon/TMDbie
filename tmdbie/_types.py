"""
Types used in TMDbie
"""

import importlib
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

_BASE = "https://api.themoviedb.org/3"

IMDB_VIDEO_BASE = "http://www.imdb.com/title/{}/videogallery"

class Endpoints:
    BASE = "https://api.themoviedb.org/3/"
    POSTER_BASE = "https://image.tmdb.org/t/p/w500"
    BACKDROP_BASE = "https://image.tmdb.org/t/p/w780"
    
    class Search:
        MOVIE = _BASE + "/search/movie"
        MULTI = _BASE + "/search/multi"
        PEOPLE = _BASE + "/search/person"
        TVSHOW = _BASE + "/search/tv"
        KEYWORD = _BASE + "/search/keyword"
        COLLECTION = _BASE + "/search/collection"
        COMPANY = _BASE + "/search/company"

    class Discover:
        MOVIE = _BASE + "/discover/movie"
        TV = _BASE + "/discover/tv"


    class Movie:
        DETAILS = _BASE + "/movie/{id}"
        VIDEOS = _BASE + "/movie/{id}/videos"

    class People:
        DETAILS = _BASE + "/person/{id}"
        EXTERNAL_IDS = _BASE + "/person/{id}/external_ids"

    class TVShow:
        DETAILS = _BASE + "/tv/{id}"
        EXTERNAL_IDS = _BASE + "/tv/{id}/external_ids"


class Movie:
    __slots__ = (
        "poster", "adult", "overview", "release_date",
        "original_title", "genre_ids", "id", "media_type",
        "original_language", "title", "backdrop", "popularity",
        "vote_count", "video", "vote_average", "imdb_id", "trailer",
        "genres", "name"
    )

    def __init__(self, **kwargs):
        self._set_attributes(**kwargs)

    def _set_attributes(self, **kwargs):
        for arg, value in kwargs.items():
            if arg == "imdb_id":
                self.__setattr__("trailer", IMDB_VIDEO_BASE.format(value))
                self.__setattr__(arg, value)
            elif arg == "poster_path":
                self.__setattr__("poster", Endpoints.POSTER_BASE + value)
            elif arg == "backdrop_path":
                self.__setattr__("backdrop", Endpoints.BACKDROP_BASE + value)
            elif arg == "genres":
                genres = [name.get("name") for name in value]
                self.__setattr__(arg, genres)
            elif arg in ["name", "title"]:
                self.__setattr__("name", value)
                self.__setattr__("title", value)

            else:
                try:
                    self.__setattr__(arg, value)
                except AttributeError:
                    pass


class TVShow:
    __slots__ = (
        "poster", "adult", "overview", "first_air_date",
        "popularity", "id", "backdrop", "vote_average", "media_type",
        "origin_country", "genre_ids", "original_language", "vote_count",
        "name", "title", "original_name", "imdb_id", "seasons", "trailer", "genres",
        "runtime"
    )

    def __init__(self, **kwargs):
        self._set_attributes(**kwargs)

    def _set_attributes(self, **kwargs):
        for arg, value in kwargs.items():
            if arg == "imdb_id":
                self.__setattr__("trailer", IMDB_VIDEO_BASE.format(value))
                self.__setattr__(arg, value)
            elif arg == "poster_path":
                self.__setattr__("poster", Endpoints.POSTER_BASE + value)
            elif arg == "backdrop_path":
                self.__setattr__("backdrop", Endpoints.BACKDROP_BASE + value)
            elif arg == "genres":
                genres = [name.get("name") for name in value]
                self.__setattr__(arg, genres)
            elif arg in ["name", "title"]:
                self.__setattr__("name", value)
                self.__setattr__("title", value)

            else:
                try:
                    self.__setattr__(arg, value)
                except AttributeError:
                    pass



class Person:
    __slots__ = (
        "profile_path", "adult", "id", "media_type",
        "known_for", "name", "popularity", "imdb_id"
    )

    def __init__(self, **kwargs):
        self._set_attributes(**kwargs)

    def _set_attributes(self, **kwargs):
        if kwargs.get("known_for"):
            known_for = []
            for entry in kwargs.get("known_for"):
                # Check if already available in cache, otherwise instantiate
                from_cache = cache.get_from_cache(kwargs.get("id"))
                if from_cache:
                    known_for.append(from_cache)
                else:
                    item = instantiate_type(entry)
                    if item:
                        known_for.append(item)

            # Remove from dict
            kwargs.pop("known_for")
            self.__setattr__("known_for", known_for)

        for arg, value in kwargs.items():
            try:
                self.__setattr__(arg, value)
            except AttributeError:
                pass


cache = importlib.import_module("tmdbie.cache_manager").CacheManager()
instantiate_type = importlib.import_module("tmdbie.utils").instantiate_type