from django.contrib import admin

from .models import ProductCategory, Product, Supplier, Batch


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country')


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'unit')
    list_filter = ('category', )
    search_fields = ('name', )


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('name', 'supplier', 'year', 'batch_round')
    list_filter = ('product', 'year')
    search_fields = ('name', )