from rest_framework import serializers

from str.models import Tag, Partner, Engine, City


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class EngineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Engine
        fields = ['id', 'name']


class PartnerSerializer(serializers.ModelSerializer):
    parts_available = EngineSerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Partner
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'latitude', 'longitude']



