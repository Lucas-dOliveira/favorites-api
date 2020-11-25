from unittest import mock

import pytest
from rest_framework.exceptions import ValidationError

from apps.favorites.serializers import (
    CustomerSerializer,
    FavoriteListSerializer,
    FavoriteSerializer,
    ProductSerializer,
)
from tests.factories import CustomerFactory, ProductFactory

pytestmark = pytest.mark.django_db


def test_customer_serializer():
    customer = CustomerFactory()
    serializer = CustomerSerializer(customer)
    data = serializer.data

    assert "id" in data
    assert "name" in data
    assert "email" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_product_serializer():
    product = ProductFactory()

    serializer = ProductSerializer(product)
    data = serializer.data

    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@mock.patch("apps.favorites.serializers.ProductSerializer.check_product_existence")
def test_product_serializer_validate_inexistent_product(check_product_existence_mock, id):
    check_product_existence_mock.return_value = False
    request_data = {"id": id}
    serializer = ProductSerializer(data=request_data)
    with pytest.raises(ValidationError) as exc:
        serializer.is_valid(raise_exception=True)
    assert f"The id {id} wasn't found at Luizalabs products API" in str(exc)
    check_product_existence_mock.assert_called_once()
    assert str(check_product_existence_mock.call_args[0][0]) == id


@mock.patch("apps.favorites.serializers.ProductSerializer.check_product_existence")
def test_product_serializer_validate_existent_product(check_product_existence_mock, id):
    check_product_existence_mock.return_value = True
    request_data = {"id": id}
    serializer = ProductSerializer(data=request_data)
    assert serializer.is_valid(raise_exception=True)
    assert "id" in serializer.data
    check_product_existence_mock.assert_called_once()
    assert str(check_product_existence_mock.call_args[0][0]) == id


def test_favorites_serializer_with_inexistent_product(id):
    request_data = {"id": id}
    serializer = FavoriteSerializer(data=request_data)
    with pytest.raises(ValidationError) as exc:
        serializer.is_valid(raise_exception=True)
    assert "Given id does not exists" in str(exc)


def test_favorites_serializer_with_existent_product():
    product = ProductFactory()
    request_data = {"id": product.id}
    serializer = FavoriteSerializer(data=request_data)
    assert serializer.is_valid(raise_exception=True)
    assert "id" in serializer.data


def test_favorites_list_serializer(luizalabs_product):
    serializer = FavoriteListSerializer(luizalabs_product)
    data = serializer.data

    assert "id" in data
    assert "title" in data
    assert "price" in data
    assert "image" in data
    assert "brand" in data
