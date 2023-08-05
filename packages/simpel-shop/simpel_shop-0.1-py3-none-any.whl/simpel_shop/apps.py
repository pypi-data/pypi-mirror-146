from django.apps import AppConfig


class SimpelShopConfig(AppConfig):
    icon = "shopping-outline"
    default_auto_field = "django.db.models.BigAutoField"
    name = "simpel_shop"
    verbose_name = "Shop"

    def ready(self):
        from django.contrib import admin

        from .models import CartItem
        from .settings import shop_settings

        if shop_settings.ADMIN:
            admin.site.register(CartItem, shop_settings.SHOP_ADMIN)
