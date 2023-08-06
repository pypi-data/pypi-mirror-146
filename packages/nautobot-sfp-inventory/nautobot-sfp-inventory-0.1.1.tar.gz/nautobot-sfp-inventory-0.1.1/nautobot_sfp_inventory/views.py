from builtins import type

from django.db.models import Q, Count

from nautobot.core.views import generic
from . import tables, forms
from .models import SFPType, SFP
from .filters import SFPTypeFilterSet, SFPFilterSet
from .tables import SFPTable


class SFPTypeListView(generic.ObjectListView):
    queryset = SFPType.objects.annotate(
        unassigned_sfps=Count('sfps', filter=Q(sfps__assigned_device__isnull=True))
    )
    table = tables.SFPTypeTable

    filterset = SFPTypeFilterSet
    filterset_form = forms.SFPTypeFilterForm



class SFPTypeView(generic.ObjectView):
    queryset = SFPType.objects.all()

    def get_extra_context(self, request, instance):
        used_sfps = SFP.objects.filter(
            assigned_device__isnull=False,
            type=instance,
        )

        unused_sfps = SFP.objects.filter(
            assigned_device__isnull=True,
            type=instance,
        )

        unused_sfp_table = SFPTable(unused_sfps)

        return {
            "unused_sfp_table": unused_sfp_table,
            "count_used_sfps": len(used_sfps),
            "count_unused_sfps": len(unused_sfps),
        }

class SFPTypeEditView(generic.ObjectEditView):
    queryset = SFPType.objects.all()
    model_form = forms.SFPTypeForm


class SFPTypeDeleteView(generic.ObjectDeleteView):
    queryset = SFPType.objects.all()


class SFPTypeBulkImportView(generic.BulkImportView):
    queryset = SFPType.objects.all()
    model_form = forms.SFPTypeCSVForm
    table = tables.SFPTypeTable


class SFPTypeBulkDeleteView(generic.BulkDeleteView):
    queryset = SFPType.objects.all()
    table = tables.SFPTypeTable


class SFPListView(generic.ObjectListView):
    queryset = SFP.objects.all()
    table = tables.SFPTable

    filterset = SFPFilterSet
    filterset_form = forms.SFPFilterForm

class SFPView(generic.ObjectView):
    queryset = SFP.objects.all()


class SFPEditView(generic.ObjectEditView):
    queryset = SFP.objects.all()
    model_form = forms.SFPForm


class SFPDeleteView(generic.ObjectDeleteView):
    queryset = SFP.objects.all()


class SFPBulkImportView(generic.BulkImportView):
    queryset = SFP.objects.all()
    model_form = forms.SFPCSVForm
    table = tables.SFPTable


class SFPBulkDeleteView(generic.BulkDeleteView):
    queryset = SFP.objects.all()
    table = tables.SFPTable
