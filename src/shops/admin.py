from django.contrib import admin
from .models import BentoShop


@admin.register(BentoShop)
class BentoShopAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'business_status',
        'stock_status',
        'updated_at',
    )
    list_filter = (
        'business_status',
        'stock_status',
    )
    search_fields = (
        'name',
        'address',
    )

    