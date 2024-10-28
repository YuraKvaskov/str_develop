from django.contrib import admin
from django.utils.html import format_html

from str.models import Banner
from .models import (
    EngineCat,
    Material,
    Group,
    SparePart,
    SparePartImage,
    RepairKit,
    RepairKitPart, RepairKitImage
)


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('image', 'created_at')

# Inline для изображений запчастей
class SparePartImageInline(admin.TabularInline):
    model = SparePartImage
    extra = 1

# Inline для частей ремкомплекта
class RepairKitPartInline(admin.TabularInline):
    model = RepairKitPart
    extra = 1

# Inline для изображений ремкомплекта
class RepairKitImageInline(admin.TabularInline):
    model = RepairKitImage
    extra = 1

@admin.register(EngineCat)
class EngineCatAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'color_display')
    search_fields = ('name',)

    def color_display(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border: 1px solid #000;"></div>',
            obj.color
        )
    color_display.short_description = 'Цвет'

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(SparePart)
class SparePartAdmin(admin.ModelAdmin):
    list_display = ('name', 'article', 'engine_cat')
    list_filter = ('engine_cat', 'groups')
    search_fields = ('name', 'article')
    inlines = [SparePartImageInline]
    filter_horizontal = ('groups',)

@admin.register(RepairKit)
class RepairKitAdmin(admin.ModelAdmin):
    list_display = ('name', 'article', 'engine_cat')
    list_filter = ('engine_cat', 'groups')
    search_fields = ('name', 'article')
    inlines = [RepairKitPartInline, RepairKitImageInline]
    filter_horizontal = ('groups',)

@admin.register(SparePartImage)
class SparePartImageAdmin(admin.ModelAdmin):
    list_display = ('spare_part', 'image_tag')
    search_fields = ('spare_part__name',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Изображение'

@admin.register(RepairKitPart)
class RepairKitPartAdmin(admin.ModelAdmin):
    list_display = ('repair_kit', 'spare_part', 'quantity')
    search_fields = ('repair_kit__name', 'spare_part__name')
    list_filter = ('repair_kit', 'spare_part')

@admin.register(RepairKitImage)
class RepairKitImageAdmin(admin.ModelAdmin):
    list_display = ('repair_kit', 'image_tag')
    search_fields = ('repair_kit__name',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Изображение'