# coding=utf-8
"""
Different utilities for TMDbie
"""
import logging
from .types import TVShow, Person, Movie
from .abstract import TMDbType

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def dict_get_by_value(dict_: dict, value):
    for k, v in dict_.items():
        if v == value:
            return k


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


media_types = {
    "tv": TVShow,
    "movie": Movie,
    "person": Person,
}


def get_media_type(data):
    if isinstance(data, dict):
        data = data.get("media_type")
    elif isinstance(data, list):
        data = data[0].get("media_type")

    if not data:
        log.error("Missing media_type")
        log.debug(data)

    real_type = media_types.get(data)
    if not real_type:
        raise TypeError("Not a valid media_type: {}".format(data))

    return real_type


def instantiate_type(data):
    if not data:
        return None

    type_ = get_media_type(data.get("media_type"))

    # Includes subclasses
    if not isinstance(type_, TMDbType):
        raise TypeError("This shouldn't happen, please notify the developer!")

    # noinspection PyCallingNonCallable
    return type_(**data)
