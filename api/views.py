from django.db.models import Q, Prefetch
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from rest_framework import generics, filters, viewsets
from rest_framework import status
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response

from catalog.models import RepairKit, SparePart, RepairKitPart, Group, Material, EngineCat
from str.models import Tag, Partner, City, Banner
from .filters import PartnerFilter, CityFilter
from .pagination import CatalogPagination
from .schema_descriptions import repair_kit_search_example, repair_kit_filter_example, spare_part_search_example, spare_part_filter_example

from .serializers import TagSerializer, PartnerSerializer, CitySerializer, RepairKitSerializer, \
    SparePartSerializer, CatalogItemSerializer, RepairKitListSerializer, SparePartListSerializer, GroupSerializer, \
    MaterialSerializer, EngineCatSerializer, BannerSerializer, OrderRequestSerializer

import logging


logger = logging.getLogger(__name__)


class OrderRequestView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = OrderRequestSerializer(data=request.data)
            if serializer.is_valid():
                logger.debug(f"Данные перед сохранением: {serializer.validated_data}")
                order = serializer.save()
                logger.info(
                    f"Новый заказ от {order.recipient_name}, адрес: {order.delivery_address}, телефон: {order.phone_number}"
                )
                return Response({"message": "Запрос успешно отправлен!"}, status=status.HTTP_201_CREATED)

            logger.warning(f"Ошибка валидации: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception(f"Ошибка при обработке запроса: {e}")
            return Response({'detail': 'Internal Server Error'}, status=500)


class BannerView(APIView):
    def get(self, request):
        banner = Banner.objects.last()
        serializer = BannerSerializer(banner, context={'request': request})
        return Response(serializer.data)


class TagListCreate(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


@method_decorator(cache_page(60 * 60), name='dispatch')  # кэш 1 час
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
        engines = EngineCat.objects.all()
        serializer = EngineCatSerializer(engines, many=True)
        return Response(serializer.data)


class EngineDetailAPIView(APIView):
    """
    Retrieve an engine instance.
    """
    def get_object(self, pk):
        try:
            return EngineCat.objects.get(pk=pk)
        except EngineCat.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        engine = self.get_object(pk)
        serializer = EngineCatSerializer(engine)
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
    queryset = SparePart.objects.all().prefetch_related('materials', 'engine_cat', 'groups', 'images')
    serializer_class = SparePartSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'article']
    filterset_fields = {
        'engine_cat': ['exact'],
        'groups__name': ['in'],
    }
    pagination_class = CatalogPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return SparePartListSerializer
        return SparePartSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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
    pagination_class = CatalogPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return RepairKitListSerializer
        return RepairKitSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CatalogListView(APIView):
    serializer_class = CatalogItemSerializer
    pagination_class = CatalogPagination

    def get(self, request, *args, **kwargs):
        spare_parts = SparePart.objects.all()
        repair_kits = RepairKit.objects.all()

        # Получение параметров запроса
        engine_cat_ids = request.query_params.getlist('engine_cat')  # Получаем список значений engine_cat
        group_ids = request.query_params.getlist('group')  # Получаем список значений group
        search = request.query_params.get('search')
        item_type = request.query_params.get('type')

        # Фильтрация по engine_cat (если передано несколько значений)
        if engine_cat_ids:
            spare_parts = spare_parts.filter(engine_cat__id__in=engine_cat_ids)
            repair_kits = repair_kits.filter(engine_cat__id__in=engine_cat_ids)

        # Фильтрация по группам (если передано несколько значений)
        if group_ids:
            spare_parts = spare_parts.filter(groups__id__in=group_ids).distinct()
            repair_kits = repair_kits.filter(groups__id__in=group_ids).distinct()

        # Фильтрация по строке поиска (если передано)
        if search:
            spare_parts = spare_parts.filter(Q(name__icontains=search) | Q(article__icontains=search))
            repair_kits = repair_kits.filter(Q(name__icontains=search) | Q(article__icontains=search))

        # Фильтрация по типу (если передано)
        if item_type == 'spare_part':
            items = spare_parts  # Только запчасти
        elif item_type == 'repair_kit':
            items = repair_kits  # Только комплекты
        else:
            items = list(spare_parts) + list(repair_kits)  # Все вместе

        # Пагинация
        paginator = self.pagination_class()
        paginated_items = paginator.paginate_queryset(items, request)

        # Сериализация и возврат ответа
        serializer = self.serializer_class(paginated_items, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)


