from django.contrib import admin

from .models import CreditLetter, DeliveryOrder, InspectionReport


class DeliveryOrderInline(admin.TabularInline):
    model = DeliveryOrder


@admin.register(CreditLetter)
class CreditLetterAdmin(admin.ModelAdmin):
    list_display = ('document_number', 'product', 'rate')
    list_filter = ('product', )
    search_fields = ('document_number', )
    inlines = (DeliveryOrderInline, )
