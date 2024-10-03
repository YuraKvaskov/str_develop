import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Partner, City
from .utils import get_coordinates, find_closest_city, get_city_coordinates


logger = logging.getLogger(__name__)


@receiver(post_save, sender=Partner)
def geocode_partner_address_partner(sender, instance, created, **kwargs):
    if created and (instance.latitude is None or instance.longitude is None):
        logger.debug(f"Geocoding address for Partner: {instance.name}")
        address = instance.address
        latitude, longitude = get_coordinates(address)

        if latitude is not None and longitude is not None:
            instance.latitude = latitude
            instance.longitude = longitude
            instance.save(update_fields=['latitude', 'longitude'])
            logger.info(f"Set coordinates for Partner '{instance.name}': {latitude}, {longitude}")

            # Определяем ближайший город
            closest_city = find_closest_city(latitude, longitude)
            if closest_city:
                instance.city = closest_city
                instance.save(update_fields=['city'])
                logger.info(f"Assigned closest City '{closest_city.name}' to Partner '{instance.name}'")
            else:
                logger.warning(f"No closest city found for Partner '{instance.name}'")
        else:
            logger.warning(f"Could not geocode address for Partner '{instance.name}'")

@receiver(post_save, sender=City)
def set_city_coordinates_on_creation(sender, instance, created, **kwargs):
    if created and (instance.latitude is None or instance.longitude is None):
        logger.debug(f"Attempting to set coordinates for City: {instance.name}")
        latitude, longitude = get_city_coordinates(instance.name)
        if latitude is not None and longitude is not None:
            logger.debug(f"Coordinates obtained: {latitude}, {longitude}")
            instance.latitude = latitude
            instance.longitude = longitude
            instance.save(update_fields=['latitude', 'longitude'])
            logger.info(f"Coordinates set for City '{instance.name}': {latitude}, {longitude}")
        else:
            logger.warning(f"Failed to obtain coordinates for City '{instance.name}'")