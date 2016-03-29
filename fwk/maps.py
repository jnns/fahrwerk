import json

from mapbox import Geocoder, Directions

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
    directions = Directions()
    geojson = directions.directions([origin, destination], 'mapbox.driving').geojson()
    first = geojson['features'][0]
    return json.dumps(first)