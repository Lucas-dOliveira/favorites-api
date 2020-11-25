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

    assert "product_id" in data
    assert "created_at" in data
    assert "updated_at" in data


@mock.patch("apps.favorites.serializers.ProductSerializer.check_product_existence")
def test_product_serializer_validate_inexistent_product(check_product_existence_mock, product_id):
    check_product_existence_mock.return_value = False
    request_data = {"product_id": product_id}
    serializer = ProductSerializer(data=request_data)
    with pytest.raises(ValidationError) as exc:
        serializer.is_valid(raise_exception=True)
    assert f"The product_id {product_id} wasn't found at Luizalabs products API" in str(exc)
    check_product_existence_mock.assert_called_once()
    assert str(check_product_existence_mock.call_args[0][0]) == product_id


@mock.patch("apps.favorites.serializers.ProductSerializer.check_product_existence")
def test_product_serializer_validate_existent_product(check_product_existence_mock, product_id):
    check_product_existence_mock.return_value = True
    request_data = {"product_id": product_id}
    serializer = ProductSerializer(data=request_data)
    assert serializer.is_valid(raise_exception=True)
    assert "product_id" in serializer.data
    check_product_existence_mock.assert_called_once()
    assert str(check_product_existence_mock.call_args[0][0]) == product_id


def test_favorites_serializer_with_inexistent_product(product_id):
    request_data = {"product_id": product_id}
    serializer = FavoriteSerializer(data=request_data)
    with pytest.raises(ValidationError) as exc:
        serializer.is_valid(raise_exception=True)
    assert "Given product_id does not exists" in str(exc)


def test_favorites_serializer_with_existent_product():
    product = ProductFactory()
    request_data = {"product_id": product.product_id}
    serializer = FavoriteSerializer(data=request_data)
    assert serializer.is_valid(raise_exception=True)
    assert "product_id" in serializer.data


def test_favorites_list_serializer(detailed_product):
    serializer = FavoriteListSerializer(detailed_product)
    data = serializer.data

    assert "id" in data
    assert "title" in data
    assert "price" in data
    assert "image" in data
    assert "brand" in data
