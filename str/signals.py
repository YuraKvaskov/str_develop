import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Partner, City
from .utils import get_coordinates, find_closest_city, get_city_coordinates


logger = logging.getLogger(__name__)


@receiver(post_save, sender=Partner)
def geocode_partner_address(sender, instance, created, **kwargs):
    if created and not instance.latitude and not instance.longitude:
        address = instance.address
        latitude, longitude = get_coordinates(address)

        if latitude is not None and longitude is not None:
            instance.latitude = latitude
            instance.longitude = longitude
            instance.save()

            # После сохранения партнёра, пытаемся определить ближайший город
            closest_city = find_closest_city(latitude, longitude)
            if closest_city:
                instance.city = closest_city
                instance.save()


@receiver(post_save, sender=City)
def set_city_coordinates_on_creation(sender, instance, created, **kwargs):
    if created and (instance.latitude is None or instance.longitude is None):
        latitude, longitude = get_city_coordinates(instance.name)
        logger.info(f'Coordinates for {instance.name}: {latitude}, {longitude}')
        if latitude and longitude:
            instance.latitude = latitude
            instance.longitude = longitude
            instance.save()