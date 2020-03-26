from django.contrib import admin

from .models import DeliveryOrder, OrderAllocation, InspectionReport


class OrderAllocationInline(admin.TabularInline):
    model = OrderAllocation


class InspectionReportInline(admin.StackedInline):
    model = InspectionReport
    extra = 0


@admin.register(DeliveryOrder)
class DeliveryOrderAdmin(admin.ModelAdmin):
    list_display = (
        'lc_number', 'supplier', 'vessel',
        'product', 'rate', 'created_at'
    )
    list_filter = ('supplier', 'product', 'created_at')
    search_fields = ('lc_number', 'vessel')
    inlines = (OrderAllocationInline, InspectionReportInline)
