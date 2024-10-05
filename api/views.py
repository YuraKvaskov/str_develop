from itertools import chain

from django.db.models import Q, Prefetch
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from rest_framework import generics, filters, viewsets

from rest_framework.views import APIView
from rest_framework.response import Response

from catalog.models import RepairKit, SparePart, RepairKitPart, Group, Material, EngineCat
from str.models import Tag, Partner, Engine, City
from .filters import PartnerFilter, CityFilter
from .schema_descriptions import repair_kit_search_example, repair_kit_filter_example, spare_part_search_example, spare_part_filter_example

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


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(name='search', description='Поиск по названию или артикулу', required=False, type=str, examples=[spare_part_search_example]),
            OpenApiParameter(name='engine_cat', description='Фильтрация по категории двигателя', required=False, type=int, examples=[spare_part_filter_example]),
            OpenApiParameter(name='groups__name', description='Фильтрация по группам запчастей', required=False, type=str, examples=[spare_part_filter_example]),
        ],
        examples=[
            spare_part_search_example,
            spare_part_filter_example,
        ]
    )
)
class SparePartViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SparePart.objects.all().prefetch_related('materials', 'engine_cat', 'groups', 'images')
    serializer_class = SparePartSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'article']
    filterset_fields = {
        'engine_cat': ['exact'],
        'groups__name': ['in'],
    }

    def get_serializer_class(self):
        if self.action == 'list':
            return SparePartListSerializer
        return SparePartSerializer


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(name='search', description='Поиск по названию или артикулу', required=False, type=str, examples=[repair_kit_search_example]),
            OpenApiParameter(name='engine_cat', description='Фильтрация по категории двигателя', required=False, type=int, examples=[repair_kit_filter_example]),
            OpenApiParameter(name='groups__name', description='Фильтрация по группам запчастей', required=False, type=str, examples=[repair_kit_filter_example]),
        ],
        examples=[
            repair_kit_search_example,
            repair_kit_filter_example,
        ]
    )
)
class RepairKitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RepairKit.objects.all().prefetch_related('materials', 'engine_cat', 'groups', 'images').prefetch_related(
        Prefetch('repairkitpart_set', queryset=RepairKitPart.objects.select_related('spare_part'))
    )
    serializer_class = RepairKitSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'article']
    filterset_fields = {
        'engine_cat': ['exact'],
        'groups__name': ['in'],
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
        'groups': ['in'],  # Фильтр по ID групп
    }
    search_fields = ['name', 'article']

    def get_queryset(self):
        spare_parts = SparePart.objects.all()
        repair_kits = RepairKit.objects.all()

        # Фильтрация по параметрам запроса
        engine_cat_id = self.request.query_params.get('engine_cat')
        group_ids = self.request.query_params.get('group')
        search = self.request.query_params.get('search')

        if engine_cat_id:
            spare_parts = spare_parts.filter(engine_cat_id=engine_cat_id)
            repair_kits = repair_kits.filter(engine_cat_id=engine_cat_id)

        if group_ids:
            group_ids = group_ids.split(',')
            spare_parts = spare_parts.filter(groups__id__in=group_ids).distinct()
            repair_kits = repair_kits.filter(groups__id__in=group_ids).distinct()

        if search:
            spare_parts = spare_parts.filter(Q(name__icontains=search) | Q(article__icontains=search))
            repair_kits = repair_kits.filter(Q(name__icontains=search) | Q(article__icontains=search))

        # Объединение двух QuerySet с использованием chain
        return chain(spare_parts, repair_kits)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)