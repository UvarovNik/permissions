import django_filters
from django_filters import rest_framework as filters

from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    status = django_filters.CharFilter(lookup_expr='iexact')
    creator = django_filters.NumberFilter(field_name='creator__id')
    created_at = django_filters.DateFromToRangeFilter(field_name='created_at')

    class Meta:
        model = Advertisement
        fields = ('status', 'creator', 'created_at')
