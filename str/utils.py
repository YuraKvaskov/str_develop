# from decimal import Decimal
# import math
# import requests
# from .models import City
# import logging
#
#
# logger = logging.getLogger(__name__)
#
#
# def get_coordinates(address):
#     api_key = 'ce6cab7e-5c86-4204-85bb-b90c99d28cd4'
#     url = f'https://geocode-maps.yandex.ru/1.x/?apikey={api_key}&geocode={address}&format=json'
#     response = requests.get(url)
#     data = response.json()
#     found_objects = int(data['response']['GeoObjectCollection']['metaDataProperty']['GeocoderResponseMetaData']['found'])
#
#     if found_objects > 0:
#         coordinates = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
#         latitude_str, longitude_str = coordinates.split()
#         latitude = Decimal(latitude_str)
#         longitude = Decimal(longitude_str)
#         return latitude, longitude
#     return None, None
#
#
# def find_closest_city(latitude, longitude):
#     closest_city = None
#     min_distance = float('inf')
#
#     all_cities = City.objects.all()
#     for city in all_cities:
#         city_latitude = Decimal(city.latitude)
#         city_longitude = Decimal(city.longitude)
#
#         # Вычисляем евклидово расстояние между текущей и целевой точками
#         lat_diff = city_latitude - latitude
#         lon_diff = city_longitude - longitude
#         distance = math.sqrt(lat_diff ** 2 + lon_diff ** 2)
#
#         if distance < min_distance:
#             min_distance = distance
#             closest_city = city
#
#     return closest_city
#
#
# def get_city_coordinates(city_name):
#     api_key = 'ce6cab7e-5c86-4204-85bb-b90c99d28cd4'
#     url = f'https://geocode-maps.yandex.ru/1.x/?apikey={api_key}&geocode={city_name}&format=json'
#     response = requests.get(url)
#
#     if response.status_code == 200:
#         data = response.json()
#         found_objects = int(
#             data['response']['GeoObjectCollection']['metaDataProperty']['GeocoderResponseMetaData']['found'])
#
#         if found_objects > 0:
#             coordinates = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
#             longitude, latitude = map(float, coordinates.split())  # Изменен порядок координат
#             logger.info(f"Found coordinates for {city_name}: {latitude}, {longitude}")
#             return latitude, longitude  # Широта, долгота
#         else:
#             logger.warning(f"No coordinates found for {city_name}")
#             return None, None
#     else:
#         logger.error(f"Error fetching data from Yandex API: {response.status_code}")
#         return None, None
