from django.forms import DateField

from nautobot.dcim.models import Manufacturer, Device
from nautobot.extras.forms import CustomFieldModelCSVForm, CustomFieldModelForm, RelationshipModelForm, \
    CustomFieldFilterForm
from .models import SFPType, SFP
from nautobot.utilities.forms import BootstrapMixin, DynamicModelMultipleChoiceField, TagFilterField, SlugField
from nautobot.utilities.forms import widgets
from nautobot.tenancy.models import Tenant
from nautobot.utilities.forms import DynamicModelChoiceField
from nautobot.utilities.forms import CSVModelChoiceField
from django import forms


class SFPTypeFilterForm(BootstrapMixin, CustomFieldFilterForm):
    model = SFPType
    q = forms.CharField(required=False, label="Search")

    manufacturer = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        to_field_name="slug",
        required=False,
        null_option="None",
    )
    tag = TagFilterField(model)


class SFPTypeForm(BootstrapMixin, CustomFieldModelForm, RelationshipModelForm):
    end_of_manufacturer_support = DateField(
        widget=widgets.DatePicker,
        required=False
    )

    class Meta:
        model = SFPType
        fields = [
            "name",
            "slug",
            "manufacturer",
            "supplier",
            "end_of_manufacturer_support",
        ]


class SFPTypeCSVForm(CustomFieldModelCSVForm):
    manufacturer = CSVModelChoiceField(
        queryset=Manufacturer.objects.all(),
        to_field_name="name",
        required=True,
    )

    class Meta:
        model = SFPType
        fields = [
            "name",
            "slug",
            "manufacturer",
            "supplier",
            "end_of_manufacturer_support",
        ]


class SFPFilterForm(BootstrapMixin, CustomFieldFilterForm):
    model = SFP
    q = forms.CharField(required=False, label="Search")

    type = DynamicModelMultipleChoiceField(
        queryset=SFPType.objects.all(),
        to_field_name="slug",
        required=False,
        null_option="None",
    )

    tenant = DynamicModelMultipleChoiceField(
        queryset=Tenant.objects.all(),
        to_field_name="slug",
        required=False,
        null_option="None",
    )

    assigned_device = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        to_field_name="name",
        required=False,
        null_option="None",
        label="Assigned Device"
    )

    tag = TagFilterField(model)


class SFPForm(BootstrapMixin, CustomFieldModelForm, RelationshipModelForm):
    tenant = DynamicModelChoiceField(queryset=Tenant.objects.all(), required=False)
    type = DynamicModelChoiceField(queryset=SFPType.objects.all(), required=False)
    assigned_device = DynamicModelChoiceField(queryset=Device.objects.all(), required=False)

    class Meta:
        model = SFP
        fields = [
            "serial_number",
            "type",
            "dc_tag",
            "asset_tag",
            "tenant",
            "assigned_device"
        ]


class SFPCSVForm(CustomFieldModelCSVForm):
    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        to_field_name="name",
        help_text="Assigned tenant",
    )

    type = CSVModelChoiceField(
        queryset=SFPType.objects.all(),
        to_field_name="slug",
        required=True,
    )

    assigned_device = CSVModelChoiceField(
        queryset=Device.objects.all(),
        to_field_name="name",
        required=False,
    )

    class Meta:
        model = SFP
        fields = [
            "serial_number",
            "type",
            "dc_tag",
            "asset_tag",
            "tenant",
            "assigned_device"
        ]
