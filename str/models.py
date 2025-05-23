import os
import requests
import logging

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone

from catalog.models import EngineCat

logger = logging.getLogger(__name__)


class Banner(models.Model):
    image = models.ImageField(upload_to='heads/')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.image:
            timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
            filename = os.path.basename(self.image.name)
            new_filename = f"Head_{timestamp}_{filename}"
            self.image.name = f'heads/{new_filename}'

        super().save(*args, **kwargs)


class City(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_city_coordinates(self, city_name):
        api_key = 'ce6cab7e-5c86-4204-85bb-b90c99d28cd4'
        url = f'https://geocode-maps.yandex.ru/1.x/?apikey={api_key}&geocode={city_name}&format=json'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            found_objects = int(
                data['response']['GeoObjectCollection']['metaDataProperty']['GeocoderResponseMetaData']['found'])

            if found_objects > 0:
                coordinates = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
                longitude, latitude = map(float, coordinates.split())  # Изменен порядок координат
                logger.info(f"Found coordinates for {city_name}: {latitude}, {longitude}")
                return latitude, longitude  # Широта, долгота
            else:
                logger.warning(f"No coordinates found for {city_name}")
                return None, None
        else:
            logger.error(f"Error fetching data from Yandex API: {response.status_code}")
            return None, None

    def save(self, *args, **kwargs):
        # Проверяем, заданы ли координаты
        if not self.latitude or not self.longitude:
            logger.debug(f"Attempting to set coordinates for City: {self.name}")
            latitude, longitude = self.get_city_coordinates(self.name)

            if latitude is not None and longitude is not None:
                self.latitude = latitude
                self.longitude = longitude
                logger.info(f"Coordinates set for City '{self.name}': {latitude}, {longitude}")
            else:
                logger.warning(f"Failed to obtain coordinates for City '{self.name}'")

        super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7,
                             blank=True,
                             null=True)
    image = models.ImageField(
        upload_to='tag_images/', null=True, blank=True)

    def __str__(self):
        return self.name


class Partner(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to='partner_images/', null=True, blank=True)
    address = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    phone = models.CharField(max_length=20)
    website = models.URLField(blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    parts_available = models.ManyToManyField(EngineCat, related_name='partners', blank=True)
    time_open_weekdays = models.TimeField(null=True, blank=True)
    time_close_weekdays = models.TimeField(null=True, blank=True)
    time_open_saturday = models.TimeField(null=True, blank=True)
    time_close_saturday = models.TimeField(null=True, blank=True)
    time_open_sunday = models.TimeField(null=True, blank=True)
    time_close_sunday = models.TimeField(null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name='partners')

    def __str__(self):
        return self.name


@receiver(post_save, sender=Partner)
def geocode_partner_address(sender, instance, created, **kwargs):
    if created:
        address = instance.address
        api_key = 'ce6cab7e-5c86-4204-85bb-b90c99d28cd4'
        response = requests.get(
            f'https://geocode-maps.yandex.ru/1.x/?apikey={api_key}&geocode={address}&format=json')
        data = response.json()
        found_objects = int(
            data['response']['GeoObjectCollection']['metaDataProperty']['GeocoderResponseMetaData']['found'])
        if found_objects > 0:
            coordinates = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
            longitude, latitude = map(float, coordinates.split())  # Поменяйте порядок!
            instance.latitude = latitude
            instance.longitude = longitude
            instance.save()


class OrderRequest(models.Model):
    recipient_name = models.CharField("Имя получателя", max_length=255)
    delivery_address = models.CharField("Адрес доставки", max_length=500)
    phone_number = models.CharField("Телефон", max_length=20, blank=True, null=True)
    created_at = models.DateTimeField("Дата запроса", auto_now_add=True)

    def __str__(self):
        return f"{self.recipient_name} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"

    class Meta:
        verbose_name = "Запрос на каталог"
        verbose_name_plural = "Запросы на каталог"
        ordering = ['-created_at']