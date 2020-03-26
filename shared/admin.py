from django.contrib import admin

from .models import Customer, Location, Union, ProductCategory, Product, \
    Supplier


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'region')
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


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country')


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category', )
    search_fields = ('name', )
