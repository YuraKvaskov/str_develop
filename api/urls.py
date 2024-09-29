from django.urls import path, include

from .views import PartnerListView, PartnerDetailView, EngineListAPIView, EngineDetailAPIView, CityListView, \
    CityDetailView, TagListView

app_name = 'api'

urlpatterns = [
    path('partners/', PartnerListView.as_view(), name='partner-list'),
    path('partners/<int:pk>/', PartnerDetailView.as_view(), name='partner-detail'),
    path('engines/', EngineListAPIView.as_view(), name='engine-list'),
    path('engines/<int:pk>/', EngineDetailAPIView.as_view(), name='engine-detail'),
    path('cities/', CityListView.as_view(), name='city-list'),
    path('cities/<int:pk>/', CityDetailView.as_view(), name='city-detail'),
    path('tags/', TagListView.as_view(), name='tag-list'),
    path('catalog/', include('catalog.urls')),  # Добавляем маршруты приложения catalog

]