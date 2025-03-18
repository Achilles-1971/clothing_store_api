from django.contrib import admin
from .models import Product, Cart, Order, OrderItem, User  # Не забудь про User


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "created_at")
    search_fields = ("name", "description")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user_id", "product", "quantity", "created_at")
    search_fields = ("user_id",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user_id", "total_price", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("user_id",)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "price")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "created_at")
    search_fields = ("username",)
