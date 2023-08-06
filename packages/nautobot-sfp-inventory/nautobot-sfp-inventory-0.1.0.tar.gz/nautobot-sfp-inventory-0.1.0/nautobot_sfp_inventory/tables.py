from nautobot.utilities.tables import ButtonsColumn, ColorColumn, ToggleColumn, BaseTable
from .models import SFPType, SFP
import django_tables2 as tables

from nautobot.tenancy.tables import TenantColumn


class SFPTypeTable(BaseTable):
    pk = ToggleColumn()
    name = tables.Column(linkify=True)
    actions = ButtonsColumn(SFPType)
    unassigned_sfps = tables.Column(verbose_name="Unassigned SFPs")

    class Meta(BaseTable.Meta):
        model = SFPType
        fields = ("pk", "name", "manufacturer", "slug", "supplier", "end_of_manufacturer_support", "unassigned_sfps", "actions")
        default_columns = (
            "pk",
            "name",
            "manufacturer",
            "supplier",
            "unassigned_sfps",
            "actions",
        )


class SFPTable(BaseTable):
    pk = ToggleColumn()
    serial_number = tables.Column(linkify=True)

    tenant = TenantColumn()
    actions = ButtonsColumn(SFP)

    class Meta(BaseTable.Meta):
        model = SFP
        fields = ("pk", "serial_number", "type", "dc_tag", "asset_tag", "tenant", "assigned_device", "actions")
        default_columns = (
            "pk", "serial_number", "type", "dc_tag", "asset_tag", "tenant", "assigned_device", "actions"
        )
