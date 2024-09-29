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
    CatalogDetailView
)

router = DefaultRouter()
router.register(r'engines', EngineCatViewSet, basename='engine')
router.register(r'materials', MaterialViewSet, basename='material')
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'spare-parts', SparePartViewSet, basename='sparepart')
router.register(r'repair-kits', RepairKitViewSet, basename='repairkit')

urlpatterns = [
    path('', include(router.urls)),
    path('catalog/', CatalogListView.as_view(), name='catalog-list'),
    path('catalog/<int:id>/', CatalogDetailView.as_view(), name='catalog-detail'),
]
