from datetime import datetime
from loguru import logger
import requests
from meteostat import Point, Daily
from config import GEOPOS_API_KEY, ResponseError
import http.client, urllib.parse
import json


def _get_point(location: str) -> tuple:
    """
    Get GEO coords by name of location
    :param location: str name of location
    :return: tuple (latitude, longitude) or error description
    """
    conn = http.client.HTTPConnection('geocode.xyz')
    logger.info(f"Request geo coordinates for *{location}*")
    params = urllib.parse.urlencode({
        'auth': GEOPOS_API_KEY,
        'locate': location,
        'json': 1
    })
    try:
        # Trying to handle all possible API errors
        conn.request('GET', '/?{}'.format(params))
        res = json.loads(conn.getresponse().read())
        print(json.dumps(res))
    except requests.exceptions.RequestException as e:
        raise SystemExit(f'Server error: {e}')
    except Exception as e:
        raise SystemExit(f'Unknown error: {e}')
    else:
        if "error" in res:
            raise ResponseError(res["error"]["description"])

        coords = tuple(map(lambda x: float(res.get(x)), ["latt", "longt"]))
        logger.info(f"Accepted coords: {coords}")
        return coords


def get_data(year: int, location: str) -> list:
    """
    Get meteo data using geo coords
    :param year: int year value
    :param location: str name of location
    :return: list of temperatures
    """
    # Set annual period

    start = datetime(year, 1, 1)
    end = datetime(year, 12, 31)

    try:
        # Propagate errors to the top level
        position = _get_point(location)
    except ResponseError as e:
        raise ResponseError(e)
    except SystemExit as e:
        raise SystemExit(e)

    point = Point(*position)
    try:
        data = Daily(point, start, end)  # Pandas DataFrame
    except Exception as e:
        SystemExit(f'Unknown error: {e}')
    else:
        # Select 'tmin','tmax' colums from Pandas DataFrame
        # and put it in one day, filtering NAN etc.
        data = data.fetch()[['tmin', 'tmax']].dropna()
        data = list(data.to_numpy().flatten())
        if len(data) < 200:
            # Too little correct data
            print(data)
            raise ResponseError("Too little correct data ")
        logger.info(f"Accepted data: {len(data)} positions")
        return data
