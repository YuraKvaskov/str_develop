# catalog/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (
    EngineCatViewSet,
    MaterialViewSet,
    GroupViewSet,
    SparePartViewSet,
    RepairKitViewSet,
    CatalogListView,
    # CatalogDetailView
)

urlpatterns = [
    path('engines/', EngineCatViewSet.as_view({'get': 'list'}), name='engine_list'),
    path('engines/<int:pk>/', EngineCatViewSet.as_view({'get': 'retrieve'}), name='engine_detail'),

    path('materials/', MaterialViewSet.as_view({'get': 'list'}), name='material_list'),
    path('materials/<int:pk>/', MaterialViewSet.as_view({'get': 'retrieve'}), name='material_detail'),

    path('groups/', GroupViewSet.as_view({'get': 'list'}), name='group_list'),
    path('groups/<int:pk>/', GroupViewSet.as_view({'get': 'retrieve'}), name='group_detail'),

    path('spare-parts/', SparePartViewSet.as_view({'get': 'list'}), name='sparepart_list'),
    path('spare-parts/<int:pk>/', SparePartViewSet.as_view({'get': 'retrieve'}), name='sparepart_detail'),

    path('repair-kits/', RepairKitViewSet.as_view({'get': 'list'}), name='repairkit_list'),
    path('repair-kits/<int:pk>/', RepairKitViewSet.as_view({'get': 'retrieve'}), name='repairkit_detail'),

    path('catalog/', CatalogListView.as_view(), name='catalog_list'),
]
# router = DefaultRouter()
# router.register(r'engines', EngineCatViewSet, basename='engine')
# router.register(r'materials', MaterialViewSet, basename='material')
# router.register(r'groups', GroupViewSet, basename='group')
# router.register(r'spare-parts', SparePartViewSet, basename='sparepart')
# router.register(r'repair-kits', RepairKitViewSet, basename='repairkit')
#
# urlpatterns = [
#     path('', include(router.urls)),
#     path('catalog/', CatalogListView.as_view(), name='catalog-list'),
#     # path('catalog/<int:id>/', CatalogDetailView.as_view(), name='catalog-detail'),
# ]
