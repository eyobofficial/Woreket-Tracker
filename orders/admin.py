from django.contrib import admin

from .models import Port, DeliveryOrder, Allocation, UnionAllocation, \
    Distribution, UnionDistribution


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


class UnionAllocationInline(admin.TabularInline):
    model = UnionAllocation
    extra = 0


@admin.register(Allocation)
class AllocationAdmin(admin.ModelAdmin):
    list_display = ('delivery_order', 'buyer')
    inlines = (UnionAllocationInline, )


class UnionDistributionInline(admin.TabularInline):
    model = UnionDistribution
    extra = 0


@admin.register(Distribution)
class DistributionAdmin(admin.ModelAdmin):
    list_display = ('delivery_order', 'buyer')
    inlines = (UnionDistributionInline, )
