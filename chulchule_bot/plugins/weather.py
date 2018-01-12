# -*- coding:utf-8 -*-
import requests

from slackbot import settings
DARK_SKY_API_END_POINT = 'https://api.darksky.net/forecast/'
GEO_API_END_POINT = 'https://maps.googleapis.com/maps/api/geocode/json'


class APIException(Exception):
    pass


def get_location_coordinates(location: str) -> tuple:
    response = requests.get(GEO_API_END_POINT, {'address': location})

    if response.status_code == 200:
        response_json = response.json()
        geo_data = response_json[0]['geometry']['location']
        return geo_data['lat'], geo_data['lng']
    raise APIException


def get_current_sky(location: str):
    try:
        lat, lng = get_location_coordinates(location)
    except APIException:
        return

    api_key = settings.DARK_SKY_API_KEY

    api_url = GEO_API_END_POINT + f'{api_key}/{lat},{lng}'

    response = requests.get(api_url)
    if response.status_code == 200:
        response_json = response.json()
