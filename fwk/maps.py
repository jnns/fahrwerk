import os
import json
import logging
import requests

from .util import search_for_key

logger = logging.getLogger(__name__)


def geocode(query):
    # Use the same geocoding backend as we do in the ReactJS frontend to
    # prevent problems. Photon provides better results than mapbox anyway.
    GEOCODING_URL = 'https://photon.komoot.de/api/'

    # For proximity based geocoding specify Berlin as the center
    GEOCODING_PARAMS = {
        'lang': 'de',
        'limit': 1,
        'lon': 13.37,
        'lat': 52.52,
        'q': query
    }
    r = requests.get(GEOCODING_URL, params=GEOCODING_PARAMS)
    r.raise_for_status()
    return r.json()


def directions(origin, destination):
    # pull coordinates from each GEOJSON object
    logger.info("Getting directions for:\n%s\n%s" % (origin, destination))
    coordinates = map(search_for_key, [origin, destination], ['coordinates'] * 2)
    # format coordinates to be comma-separated
    coordinates = ["{},{}".format(*i) for i in coordinates]

    DIRECTIONS_URL = 'https://api.mapbox.com/directions/v5/{profile}/{coordinates}'
    DIRECTIONS_PARAMS = {
        'profile': 'mapbox/driving',
        'coordinates': "{};{}".format(*coordinates)
    }
    r = requests.get(DIRECTIONS_URL.format(**DIRECTIONS_PARAMS),
        params={
            'access_token': os.environ.get("MAPBOX_ACCESS_TOKEN"),
            'geometries': 'geojson'
    })
    logger.info("Result: %s" % r.json())
    r.raise_for_status()
    return r.json()
