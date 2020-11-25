from uuid import uuid4

from django.db import models


class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


class Product(TimestampModel):
    serializer = "apps.favorites.serializers.ProductSerializer"
    id = models.UUIDField(primary_key=True)


class Customer(UUIDModel, TimestampModel):
    serializer = "apps.favorites.serializers.CustomerSerializer"

    email = models.EmailField(unique=True, db_index=True)
    name = models.CharField(max_length=128)
    favorites = models.ManyToManyField(Product, related_name="customer_favorites")
