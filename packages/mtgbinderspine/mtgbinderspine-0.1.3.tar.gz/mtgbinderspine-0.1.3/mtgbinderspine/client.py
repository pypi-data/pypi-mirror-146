import logging
import pathlib
import tempfile
import time

import requests
from diskcache import FanoutCache
from requests.exceptions import HTTPError

log = logging.getLogger("rich")

cache = FanoutCache(directory=pathlib.Path(tempfile.gettempdir()) / "mtgbinderspine")


@cache.memoize()
def _get_scryfall(path: str):
    log.info(f"Fetching {path}")
    response = requests.get(f"https://api.scryfall.com/{path}")
    response.raise_for_status()

    time.sleep(0.1)
    return response


@cache.memoize()
def get_memoized(uri: str):
    log.info(f"Fetching {uri}")
    response = requests.get(uri)
    response.raise_for_status()

    return response.content


def get_set_image(set_three_letter_code: str) -> bytes:
    """
    Downloads the set svg from scryfall

    The scryfall api docs request that we don't make more than 10 requests per second.
    """
    try:
        set_info = _get_scryfall(f"sets/{set_three_letter_code}").json()
    except HTTPError as e:
        if e.response.status_code == 404:
            return None

    icon_uri = set_info["icon_svg_uri"]

    return get_memoized(icon_uri)


def get_set_name(set_three_letter_code: str) -> str:
    set_info = _get_scryfall(f"sets/{set_three_letter_code}").json()

    return set_info["name"]
