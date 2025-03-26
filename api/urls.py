from django.urls import path, include

from .views import PartnerListView, PartnerDetailView, EngineListAPIView, EngineDetailAPIView, CityListView, \
    CityDetailView, TagListView, BannerView, OrderRequestView

app_name = 'api'

urlpatterns = [
    path('partners/', PartnerListView.as_view(), name='partner_list'),
    path('partners/<int:pk>/', PartnerDetailView.as_view(), name='partner_detail'),
    path('engines/', EngineListAPIView.as_view(), name='engine_list'),
    path('engines/<int:pk>/', EngineDetailAPIView.as_view(), name='engine_detail'),
    path('cities/', CityListView.as_view(), name='city_list'),
    path('cities/<int:pk>/', CityDetailView.as_view(), name='city_detail'),
    path('tags/', TagListView.as_view(), name='tag_list'),
    path('catalog/', include('catalog.urls')),  # Добавляем маршруты приложения catalog
    path('head/', BannerView.as_view(), name='head'),
    path('order-request/', OrderRequestView.as_view(), name='order_request'),

]