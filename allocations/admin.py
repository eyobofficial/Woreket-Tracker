from django.contrib import admin

from .models import LC, DistributionOrder, Allocation, Fertilizer


@admin.register(LC)
class LCAdmin(admin.ModelAdmin):
    list_display = ('document_number', )


@admin.register(Fertilizer)
class FertilizerAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(DistributionOrder)
class DistributionOrderAdmin(admin.ModelAdmin):
    list_display = ('vessel', 'lc', 'status', 'created_by')
    list_filter = ('status', )


@admin.register(Allocation)
class AllocationAdmin(admin.ModelAdmin):
    list_display = (
        'union', 'distribution_order',
        'location', 'region', 'quantity'
    )
    list_filter = ('region', )
