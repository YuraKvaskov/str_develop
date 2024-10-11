from django.urls import path
from api.views import (
    EngineCatViewSet,
    MaterialViewSet,
    GroupViewSet,
    SparePartViewSet,
    RepairKitViewSet,
    CatalogListView,
)

urlpatterns = [
    path('engine/', EngineCatViewSet.as_view({'get': 'list'}), name='engine_list'),
    path('engine/<int:pk>/', EngineCatViewSet.as_view({'get': 'retrieve'}), name='engine_detail'),

    path('material/', MaterialViewSet.as_view({'get': 'list'}), name='material_list'),
    path('material/<int:pk>/', MaterialViewSet.as_view({'get': 'retrieve'}), name='material_detail'),

    path('group/', GroupViewSet.as_view({'get': 'list'}), name='group_list'),
    path('group/<int:pk>/', GroupViewSet.as_view({'get': 'retrieve'}), name='group_detail'),

    path('spare_part/', SparePartViewSet.as_view({'get': 'list'}), name='sparepart_list'),
    path('spare_part/<int:pk>/', SparePartViewSet.as_view({'get': 'retrieve'}), name='sparepart_detail'),

    path('repair_kit/', RepairKitViewSet.as_view({'get': 'list'}), name='repairkit_list'),
    path('repair_kit/<int:pk>/', RepairKitViewSet.as_view({'get': 'retrieve'}), name='repairkit_detail'),

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
