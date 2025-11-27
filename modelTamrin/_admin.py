from django.contrib import admin
from .models import (
    Category,
    PromotionEvent,
    Product,
    ProductPromotionEvent,
    StockManagement,
    User,
    Order,
    OrderProduct,
)


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'is_active', 'level']
    list_filter = ['is_active', 'level']
    search_fields = ['name', 'slug']


@admin.register(PromotionEvent)
class PromotionEventAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'price_reduction']
    list_filter = ['start_date', 'end_date']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'price', 'is_active', 'is_digital', 'created_at']
    list_filter = ['is_active', 'is_digital', 'category', 'created_at']
    search_fields = ['name', 'slug', 'description']


@admin.register(ProductPromotionEvent)
class ProductPromotionEventAdmin(admin.ModelAdmin):
    list_display = ['product', 'promotion_event']
    list_filter = ['promotion_event']
    search_fields = ['product__name', 'promotion_event__name']


@admin.register(StockManagement)
class StockManagementAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'last_checked_at']
    list_filter = ['last_checked_at']
    search_fields = ['product__name']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']
    search_fields = ['username', 'email']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'user__email']


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity']
    list_filter = ['order', 'product']
    search_fields = ['order__id', 'product__name']
