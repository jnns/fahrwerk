import json
import logging

from mapbox import Geocoder, Directions

logger = logging.getLogger(__name__)

# For proximity based geocoding specify Berlin as the center
FILTERS = {
    'types': ['address', 'place'],
    'country': ['de'],
    'lon': 13.37, 'lat': 52.52,
}

def geocode(query):
    geocoder = Geocoder()

    response = geocoder.forward(query, **FILTERS)
    first = response.geojson()['features'][0]
    return first


def directions(origin, destination):
    try:
        directions = Directions()
        logger.info("Getting directions for: %s / %s" % (origin, destination))
        geojson = directions.directions([origin, destination], 'mapbox.driving').geojson()
        logger.info("Result: %s" % geojson)
        first = geojson['features'][0]
    except Exception as e:
        first = str(e)
    return json.dumps(first)