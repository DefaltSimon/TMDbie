"""

TMDbie - A python 3.5+ library for getting film info.
Uses https://www.themoviedb.org

"""


__author__ = "DefaltSimon"
__version__ = "1.0.0"
__license__ = "MIT"

from ._types import Person, TVShow, Movie, Endpoints
from .client import Client
from .exceptions import TMDbException, HTTPException, APIException, RatelimitException, DecodeError
from .connector import AioHttpConnector, UrllibConnector, RequestsConnector, Connector