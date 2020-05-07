from django.contrib import admin

from .models import Customer, Location, Union


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'code')
    search_fields = ('name', )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'customer')
    list_filter = ('customer', )
    search_fields = ('name', )


@admin.register(Union)
class UnionAdmin(admin.ModelAdmin):
    list_display = ('name', 'customer')
    list_filter = ('customer', )
    search_fields = ('name', )
