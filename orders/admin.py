from django.contrib import admin

from .models import Port, DeliveryOrder, Allocation, Distribution


@admin.register(Port)
class PortAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'is_default')
    list_filter = ('country', 'is_default')
    search_fields = ('name', 'country')


class AllocationInline(admin.TabularInline):
    model = Allocation
    extra = 0


class DistributionInline(admin.TabularInline):
    model = Distribution
    extra = 0


@admin.register(DeliveryOrder)
class DeliveryOrderAdmin(admin.ModelAdmin):
    list_display = ('lc_number', 'vessel', 'batch', 'created_at')
    list_filter = ('batch', 'created_at', 'status')
    search_fields = ('lc_number', 'vessel')
    inlines = (AllocationInline, DistributionInline)
