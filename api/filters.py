import django_filters
from django_filters import rest_framework as filters
from pytz import timezone as tz
from datetime import datetime

from catalog.models import EngineCat
from str.models import Tag, Partner, City


class PartnerFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    tags = filters.ModelMultipleChoiceFilter(field_name='tags', queryset=Tag.objects.all())
    parts_available = filters.ModelMultipleChoiceFilter(field_name='parts_available', queryset=EngineCat.objects.all())
    open_now = filters.BooleanFilter(method='filter_open_now')
    city = filters.ModelChoiceFilter(field_name='city', queryset=City.objects.all())

    class Meta:
        model = Partner
        fields = ['name', 'tags', 'parts_available', 'open_now', 'city']

    def filter_open_now(self, queryset, name, value):
        if value:
            current_time = self.get_current_time()
            open_partners = []
            for partner in queryset:
                if partner.is_open(current_time):
                    open_partners.append(partner.id)
            return queryset.filter(id__in=open_partners)
        return queryset

    def get_current_time(self):
        user_timezone = self.request.GET.get('timezone')
        user_tz = tz(user_timezone)
        return datetime.now(user_tz)


class CityFilter(filters.FilterSet):
    id = django_filters.NumberFilter(field_name='id')

    class Meta:
        model = City
        fields = ['id']