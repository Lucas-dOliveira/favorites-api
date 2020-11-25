from django.db import models

from apps.core.models import TimestampModel, UUIDModel


class Product(TimestampModel):
    serializer = "apps.favorites.serializers.ProductSerializer"
    id = models.UUIDField(primary_key=True)


class Customer(UUIDModel, TimestampModel):
    serializer = "apps.favorites.serializers.CustomerSerializer"

    email = models.EmailField(unique=True, db_index=True)
    name = models.CharField(max_length=128)
    favorites = models.ManyToManyField(Product, related_name="customer_favorites")
