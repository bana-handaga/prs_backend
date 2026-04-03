import django_filters
from .models import AttendanceRecord


class AttendanceFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(field_name='date')
    date_from = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    month = django_filters.CharFilter(method='filter_month')
    department = django_filters.NumberFilter(field_name='staff__department')
    staff_id = django_filters.NumberFilter(field_name='staff')

    class Meta:
        model = AttendanceRecord
        fields = ['status', 'is_overtime']

    def filter_month(self, queryset, name, value):
        # value format: YYYY-MM
        try:
            year, month = value.split('-')
            return queryset.filter(date__year=int(year), date__month=int(month))
        except (ValueError, AttributeError):
            return queryset
