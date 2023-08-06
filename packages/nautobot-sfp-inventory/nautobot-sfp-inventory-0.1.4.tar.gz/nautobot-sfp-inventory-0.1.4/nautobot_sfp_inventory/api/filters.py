import django_filters
from django.db.models import Q

from nautobot.extras.filters import CustomFieldModelFilterSet, CreatedUpdatedFilterSet
from nautobot_sfp_inventory.models import SFPType, SFP
from nautobot.utilities.filters import BaseFilterSet


class SFPTypeFilterSet(
    BaseFilterSet,
    CustomFieldModelFilterSet,
    CreatedUpdatedFilterSet,
):

    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(manufacturer__name=value) | Q(model=value))

    class Meta:
        model = SFPType
        fields = ["id", "manufacturer", "name", "slug", "supplier"]


class SFPFilterSet(
    BaseFilterSet,
    CustomFieldModelFilterSet,
    CreatedUpdatedFilterSet,
):

    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(serial_number=value) | Q(dc_tag=value) | Q(asset_tag=value))

    class Meta:
        model = SFP
        fields = ["id", "serial_number", "type", "dc_tag", "asset_tag", "assigned_device", "tenant"]
