from rest_framework import serializers

from catalog.models import RepairKit, SparePart, RepairKitPart, SparePartImage, Group, Material, EngineCat, \
    RepairKitImage
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


class EngineCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngineCat
        fields = ['id', 'name']


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'name', 'color']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class SparePartImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = SparePartImage
        fields = ['id', 'image']


class SparePartSerializer(serializers.ModelSerializer):
    images = SparePartImageSerializer(many=True, read_only=True)
    material = MaterialSerializer()
    engine = EngineSerializer()
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = SparePart
        fields = [
            'id',
            'name',
            'article',
            'material',
            'special_feature',
            'material_properties',
            'engine',
            'is_hit',
            'groups',
            'images',
        ]


class SparePartListSerializer(serializers.ModelSerializer):
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = SparePart
        fields = ['id', 'name', 'article', 'main_image']

    def get_main_image(self, obj):
        image = obj.images.first()
        if image:
            return self.context['request'].build_absolute_uri(image.image.url)
        return None


class RepairKitPartSerializer(serializers.ModelSerializer):
    spare_part = SparePartListSerializer()

    class Meta:
        model = RepairKitPart
        fields = ['spare_part', 'quantity']


class RepairKitImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairKitImage
        fields = ['id', 'image']


class RepairKitSerializer(serializers.ModelSerializer):
    images = RepairKitImageSerializer(many=True, read_only=True)
    material = MaterialSerializer()
    engine = EngineSerializer()
    groups = GroupSerializer(many=True, read_only=True)
    parts = RepairKitPartSerializer(source='repairkitpart_set', many=True, read_only=True)

    class Meta:
        model = RepairKit
        fields = [
            'id',
            'name',
            'article',
            'material',
            'special_feature',
            'material_properties',
            'engine',
            'is_hit',
            'groups',
            'images',
            'parts',
        ]


class RepairKitListSerializer(serializers.ModelSerializer):
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = RepairKit
        fields = ['id', 'name', 'article', 'main_image']

    def get_main_image(self, obj):
        image = obj.images.first()
        if image:
            return image.image.url
        return None

class CatalogItemSerializer(serializers.Serializer):
    type = serializers.CharField()
    id = serializers.IntegerField()
    name = serializers.CharField()
    article = serializers.CharField()
    main_image = serializers.URLField()

    def to_representation(self, instance):
        if isinstance(instance, SparePart):
            return {
                'type': 'spare_part',
                'id': instance.id,
                'name': instance.name,
                'article': instance.article,
                'main_image': instance.images.first().image.url if instance.images.exists() else None,
            }
        elif isinstance(instance, RepairKit):
            return {
                'type': 'repair_kit',
                'id': instance.id,
                'name': instance.name,
                'article': instance.article,
                'main_image': instance.images.first().image.url if instance.images.exists() else None,
            }
        return super().to_representation(instance)

