import datetime

import factory
from factory.django import DjangoModelFactory

from apps.favorites.models import Customer, Product


class CustomerFactory(DjangoModelFactory):
    class Meta:
        model = Customer

    name = factory.Faker("name")
    email = factory.Faker("ascii_email")
    created_at = datetime.datetime(2020, 11, 16, 16, 0, 0)
    updated_at = datetime.datetime(2020, 12, 1, 14, 30, 0)


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    product_id = factory.Faker("uuid4")
    created_at = datetime.datetime(2020, 11, 16, 16, 0, 0)
    updated_at = datetime.datetime(2020, 12, 1, 14, 30, 0)
