from django.contrib import admin

from str.models import Partner, Tag, City, OrderRequest


@admin.register(OrderRequest)
class OrderRequestAdmin(admin.ModelAdmin):
    list_display = ['recipient_name', 'delivery_address', 'phone_number', 'created_at']
    search_fields = ['recipient_name', 'phone_number', 'delivery_address']
    list_filter = ['created_at']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    search_fields = ('name',)

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'website')
    search_fields = ('name', 'address')
    list_filter = ('tags', 'parts_available')


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude')
    search_fields = ('name',)
