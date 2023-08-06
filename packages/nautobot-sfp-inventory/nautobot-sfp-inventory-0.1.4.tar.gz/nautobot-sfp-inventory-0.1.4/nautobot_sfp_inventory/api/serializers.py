from nautobot.core.api import WritableNestedSerializer
from nautobot.dcim.api.nested_serializers import NestedManufacturerSerializer, NestedDeviceSerializer
from nautobot.extras.api.customfields import CustomFieldModelSerializer
from nautobot.tenancy.api.nested_serializers import NestedTenantSerializer
from rest_framework import serializers
from nautobot_sfp_inventory.models import SFPType, SFP

class NestedRackRoleSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="plugins-api:nautobot_sfp_inventory-api:sfptype-detail")

    class Meta:
        model = SFPType
        fields = ["id", "url", "manufacturer", "model"]


class SFPTypeSerializer(CustomFieldModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="plugins-api:nautobot_sfp_inventory-api:sfptype-detail")
    manufacturer = NestedManufacturerSerializer()

    class Meta:
        model = SFPType
        fields = [
            "id",
            "url",
            "name",
            "slug",
            "manufacturer",
            "supplier",
            "end_of_manufacturer_support",
            "custom_fields",
            "created",
            "last_updated",
        ]

class SFPSerializer(CustomFieldModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="plugins-api:nautobot_sfp_inventory-api:sfp-detail")
    tenant = NestedTenantSerializer()
    type = NestedRackRoleSerializer()
    assigned_device = NestedDeviceSerializer(required=False, allow_null=True)

    class Meta:
        model = SFP
        fields = [
            "id",
            "url",
            "serial_number",
            "type",
            "dc_tag",
            "asset_tag",
            "tenant",
            "assigned_device",
            "custom_fields",
            "created",
            "last_updated",
        ]