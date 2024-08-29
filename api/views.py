from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics


from rest_framework.views import APIView
from rest_framework.response import Response

from str.models import Tag, Partner, Engine, City
from .filters import PartnerFilter, CityFilter
from .serializers import TagSerializer, PartnerSerializer, EngineSerializer, CitySerializer


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
