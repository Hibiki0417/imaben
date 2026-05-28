from django.contrib import admin
from .models import BentoShop, ShopStaff


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

@admin.register(ShopStaff)
class ShopStaffAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'shop',
        'role',
        'created_at',
    )
    list_filter = (
        'role',
        'shop',
    )
    search_fields = (
        'user__username',
        'shop__name',
    )
    