# coding=utf-8
import tmdbie
import asyncio
import time
import logging
import configparser

parser = configparser.ConfigParser()
parser.read("config.ini")

logging.basicConfig(level=logging.DEBUG)
loop = asyncio.get_event_loop()

# Insert your api key here
api_key = parser.get("tmdb", "key")

ah = time.time()
client = tmdbie.Client(api_key)
print("Instantiating took {}".format(time.time() - ah))


async def get(title):
    return await client.search_multi(title)


while True:
    name = input(">")
    resp = loop.run_until_complete(get(str(name)))

    if not resp:
        print("Not found.")
        continue

    if resp.media_type == "movie":
        print("{}, {}".format(resp.trailer, resp.genres))
        # print("{} - {} ({}) - {}\n{}".format(resp.title, resp.overview, resp.media_type, resp.poster_path, resp.id))
    elif resp.media_type == "tv":
        print("{}".format(resp.genres))
    elif resp.media_type == "person":
        print("{}, {}\n{}\n{}".format(resp.name, resp.popularity, resp.known_for, resp.id))
