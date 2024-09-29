from django.contrib import admin
from django.utils.html import format_html

from .models import (
    EngineCat,
    Material,
    Group,
    SparePart,
    SparePartImage,
    RepairKit,
    RepairKitPart
)


class SparePartImageInline(admin.TabularInline):
    model = SparePartImage
    extra = 1


@admin.register(SparePart)
class SparePartAdmin(admin.ModelAdmin):
    list_display = ('name', 'article', 'engine_cat', 'is_hit')
    list_filter = ('engine_cat', 'is_hit', 'groups')
    search_fields = ('name', 'article')
    inlines = [SparePartImageInline]
    filter_horizontal = ('groups',)


class RepairKitPartInline(admin.TabularInline):
    model = RepairKitPart
    extra = 1
    autocomplete_fields = ['spare_part']


class SparePartInline(admin.TabularInline):
    model = RepairKit.parts.through
    extra = 1


@admin.register(RepairKit)
class RepairKitAdmin(admin.ModelAdmin):
    list_display = ('name', 'article', 'engine_cat', 'is_hit')
    list_filter = ('engine_cat', 'is_hit', 'groups')
    search_fields = ('name', 'article')
    inlines = [RepairKitPartInline]
    filter_horizontal = ('groups',)
    exclude = ('parts',)


@admin.register(EngineCat)
class EngineCatAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    search_fields = ('name', 'color')

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.image.url)
        return "-"

    image_tag.short_description = 'Изображение'

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

