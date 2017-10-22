# coding=utf-8
"""
TMDbie - a python 3.5+ library for getting movie info
Developed for use in Nano, a discord bot
"""

__author__ = "DefaltSimon"
__license__ = "MIT"

# General imports
import logging
from typing import Union

# Library imports
from .connector import UrllibConnector, RequestsConnector, AioHttpConnector
from .types import Endpoints, Movie, Person, TVShow
from .utils import instantiate_type
from .cache_manager import CacheManager
from .exceptions import APIException

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class Client:
    def __init__(self, api_key: str, connector=None, cache_manager=CacheManager):
        self.api_key = str(api_key)

        self.cache = cache_manager()

        if not connector:
            self.req = AioHttpConnector()
        else:
            if connector == "aiohtp":
                self.req = AioHttpConnector()
            elif connector == "requests":
                self.req = RequestsConnector()
            elif connector == "urllib":
                self.req = UrllibConnector()
            else:
                # DANGEROUS (you must implement your own class)
                log.warning("Parameter connector was not one of aiohttp/requests/urllib, instancing with connector()")
                self.req = connector()

    async def prepare_request(self, fields=None):
        # If no other fields are required, skip the procedure
        if not fields:
            return {"api_key": self.api_key}

        # Insert api key
        if "api_key" not in fields:
            fields["api_key"] = self.api_key

        # Normalize the payload dict (remove None's)
        return {a: b for a, b in fields.items() if b is not None}

    async def search_multi(self, query: str, language=None, page=None, include_adult=None, region=None, check_cache=True) -> Union[Movie, TVShow, Person, None]:
        if not query:
            return None

        if check_cache:
            query_by_name = self.cache.get_from_cache(query)
            if query_by_name:
                log.info("Got item from cache")
                return query_by_name

        endpoint = Endpoints.Search.MULTI
        entries = await self._search_get(endpoint, query, page, instantiate_types=False, language=language, include_adult=include_adult, region=region)

        if not entries:
            return None

        first_entry = entries[0]

        type_ = first_entry.get("media_type")

        # Instantiate with additional info
        if type_ == "movie":
            additional = await self._movie_info(first_entry.get("id"))
            if not additional:
                raise APIException("no data")
            additional["media_type"] = "movie"

            result = Movie(**additional)

        elif type_ == "tv":
            additional = await self._tv_info(first_entry.get("id"))
            if not additional:
                raise APIException("no data")
            additional["media_type"] = "tv"

            result = TVShow(**additional)
        elif type_ == "person":
            # additional = await self._person_info(first_entry.get("id"))
            # if not additional:
            #     raise APIException("no data")

            result = Person(**first_entry)
        else:
            log.critical("This shouldn't happen, notify the dev!")
            return None

        self.cache.item_set(result)

        return result

    async def _search_get(self, endpoint, query=None, page=None, instantiate_types=True, **fields) -> Union[list, dict, None]:
        payload = {
            "query": query,
            "page": page,
        }

        for name, value in fields.items():
            payload[name] = value

        resp = await self._send_request(endpoint, payload)

        if not resp:
            return None
        results = resp.get("results")
        if not results:
            return None

        # Only instantiate if specified
        if instantiate_types:
            res = []
            for entry in results:
                instance = instantiate_type(entry)
                if instance:
                    res.append(instance)

            return res

        else:
            return results

    async def _movie_info(self, id_: int):
        endpoint = Endpoints.Movie.DETAILS.format(id=id_)
        return await self._send_request(endpoint)

    async def _person_info(self, id_: int):
        endpoint = Endpoints.People.DETAILS.format(id=id_)
        return await self._send_request(endpoint)

    async def _tv_info(self, id_: int):
        endpoint = Endpoints.TVShow.DETAILS.format(id=id_)
        return await self._send_request(endpoint)

    async def _send_request(self, endpoint, payload=None):
        payload = await self.prepare_request(payload)
        return await self.req.request(endpoint, payload)
