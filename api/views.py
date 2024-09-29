from django.db.models import Q, Prefetch
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, viewsets

from rest_framework.views import APIView
from rest_framework.response import Response

from catalog.models import RepairKit, SparePart, RepairKitPart, Group, Material, EngineCat
from str.models import Tag, Partner, Engine, City
from .filters import PartnerFilter, CityFilter
from .serializers import TagSerializer, PartnerSerializer, EngineSerializer, CitySerializer, RepairKitSerializer, \
    SparePartSerializer, CatalogItemSerializer, RepairKitListSerializer, SparePartListSerializer, GroupSerializer, \
    MaterialSerializer, EngineCatSerializer

import logging

logger = logging.getLogger(__name__)


class TagListCreate(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class PartnerListView(generics.ListAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PartnerFilter


class PartnerDetailView(generics.RetrieveAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer


class EngineListAPIView(APIView):
    """
    List all engines.
    """
    def get(self, request):
        engines = Engine.objects.all()
        serializer = EngineSerializer(engines, many=True)
        return Response(serializer.data)


class EngineDetailAPIView(APIView):
    """
    Retrieve an engine instance.
    """
    def get_object(self, pk):
        try:
            return Engine.objects.get(pk=pk)
        except Engine.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        engine = self.get_object(pk)
        serializer = EngineSerializer(engine)
        return Response(serializer.data)


class CityListView(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CityFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        city_id = self.request.query_params.get('id', None)
        if city_id is not None:
            queryset = queryset.filter(id=city_id)
        return queryset


class CityDetailView(generics.RetrieveAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class EngineCatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EngineCat.objects.all()
    serializer_class = EngineCatSerializer


class MaterialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class SparePartViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SparePart.objects.all().select_related('material', 'engine_cat').prefetch_related('groups', 'images')
    serializer_class = SparePartSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'article']
    filterset_fields = {
        'engine_cat': ['exact'],
        'groups__name': ['in'],
        'is_hit': ['exact'],
    }

    def get_serializer_class(self):
        if self.action == 'list':
            return SparePartListSerializer
        return SparePartSerializer


class RepairKitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RepairKit.objects.all().select_related('material', 'engine_cat').prefetch_related(
        'groups',
        'images',
        Prefetch('repairkitpart_set', queryset=RepairKitPart.objects.select_related('spare_part'))
    )
    serializer_class = RepairKitSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'article']
    filterset_fields = {
        'engine_cat': ['exact'],
        'groups__name': ['in'],
        'is_hit': ['exact'],
    }

    def get_serializer_class(self):
        if self.action == 'list':
            return RepairKitListSerializer
        return RepairKitSerializer


class CatalogListView(generics.ListAPIView):
    serializer_class = CatalogItemSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = {
        'engine_cat': ['exact'],
        'groups__name': ['in'],
        'is_hit': ['exact'],
    }
    search_fields = ['name', 'article']

    def get_queryset(self):
        spare_parts = SparePart.objects.all()
        repair_kits = RepairKit.objects.all()

        # Фильтрация по параметрам запроса
        engine_cat_id = self.request.query_params.get('engine_cat')
        is_kit = self.request.query_params.get('is_kit')
        group = self.request.query_params.get('group')
        is_hit = self.request.query_params.get('is_hit')
        search = self.request.query_params.get('search')

        if engine_cat_id:
            spare_parts = spare_parts.filter(engine_cat_id=engine_cat_id)
            repair_kits = repair_kits.filter(engine_cat_id=engine_cat_id)

        if is_kit is not None:
            if is_kit.lower() == 'true':
                spare_parts = SparePart.objects.none()
            elif is_kit.lower() == 'false':
                repair_kits = RepairKit.objects.none()

        if group:
            groups = group.split(',')
            spare_parts = spare_parts.filter(groups__name__in=groups).distinct()
            repair_kits = repair_kits.filter(groups__name__in=groups).distinct()

        if is_hit is not None:
            if is_hit.lower() == 'true':
                spare_parts = spare_parts.filter(is_hit=True)
                repair_kits = repair_kits.filter(is_hit=True)
            elif is_hit.lower() == 'false':
                spare_parts = spare_parts.filter(is_hit=False)
                repair_kits = repair_kits.filter(is_hit=False)

        if search:
            spare_parts = spare_parts.filter(Q(name__icontains=search) | Q(article__icontains=search))
            repair_kits = repair_kits.filter(Q(name__icontains=search) | Q(article__icontains=search))

        return list(spare_parts) + list(repair_kits)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


class CatalogDetailView(generics.RetrieveAPIView):
    serializer_class = SparePartSerializer  # Или RepairKitSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return SparePart.objects.all() | RepairKit.objects.all()

    def get_serializer(self, *args, **kwargs):
        instance = self.get_object()
        if isinstance(instance, SparePart):
            serializer = SparePartSerializer(instance, context={'request': self.request})
        elif isinstance(instance, RepairKit):
            serializer = RepairKitSerializer(instance, context={'request': self.request})
        return serializer


# class ProductListView(generics.ListAPIView):
#     serializer_class = ProductSerializer
#     pagination_class = PageNumberPagination
#     filter_backends = [SearchFilter]
#     search_fields = ['name', 'part_number']
#
#     def get_queryset(self):
#         queryset = Product.objects.filter(available=True)  # Фильтрация по полю available
#
#         engine_id = self.request.query_params.get('engine_id', None)
#         category_id = self.request.query_params.get('category_id', None)
#
#         if engine_id:
#             queryset = queryset.filter(engine_id=engine_id)
#
#         if category_id:
#             queryset = queryset.filter(category_id=category_id)
#
#         return queryset
#

# class ProductDetailView(generics.RetrieveAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
#
# class CategoryListAPIView(generics.ListAPIView):
#     serializer_class = CategorySerializer
#
#     def get_queryset(self):
#         engine_id = self.request.query_params.get('engine_id')
#         if engine_id:
#             queryset = Category.objects.filter(engine_id=engine_id, parent_category=None)
#         else:
#             queryset = Category.objects.filter(parent_category=None)
#         return queryset
#
#
# class CategoryDetailAPIView(generics.RetrieveAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
