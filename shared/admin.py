from django.contrib import admin

from .models import Region, Location, Union

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'region')
    list_filter = ('region', )


@admin.register(Union)
class UnionAdmin(admin.ModelAdmin):
    list_display = ('name', 'region')
    list_filter = ('region', )
