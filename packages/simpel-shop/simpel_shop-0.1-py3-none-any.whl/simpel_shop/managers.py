from django.db import models
from simpel_utils.models.paranoid import ParanoidManager


class BlueprintParameterManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class CartManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class CartItemManager(ParanoidManager):
    def get_queryset(self):
        return super().get_queryset()


class BlueprintManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
