from unittest import mock
from uuid import uuid4

import pytest
from dateutil.parser import isoparse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.reverse import reverse

from tests.factories import CustomerFactory, ProductFactory

pytestmark = pytest.mark.django_db


def test_customer_list(client_api):
    customer = CustomerFactory()
    url = reverse("favorites:customers-list")
    response = client_api.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    customer_result = response.data[0]
    assert str(customer.id) == customer_result["id"]
    assert customer.name == customer_result["name"]
    assert customer.name == customer_result["name"]
    assert isoparse(str(customer.created_at)) == isoparse(customer_result["created_at"])
    assert isoparse(str(customer.updated_at)) == isoparse(customer_result["updated_at"])


@pytest.mark.freeze_time("2020-12-07")
def test_customer_create(client_api):
    customer_payload = {"name": "Lucas de Oliveira", "email": "lucas.oliveira@magazineluiza.com.br"}

    url = reverse("favorites:customers-list")
    response = client_api.post(url, customer_payload)

    customer_result = response.data
    assert response.status_code == status.HTTP_201_CREATED
    assert customer_payload["name"] == customer_result["name"]
    assert customer_payload["email"] == customer_result["email"]
    assert "id" in customer_result
    assert customer_result["created_at"] == "2020-12-07T00:00:00Z"
    assert customer_result["updated_at"] == "2020-12-07T00:00:00Z"


def test_customer_update(client_api):
    customer = CustomerFactory()

    new_name = customer.name[::-1]

    update_payload = {"name": new_name}
    url = reverse("favorites:customers-detail", [customer.id])
    response = client_api.patch(url, update_payload)

    customer.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert customer.name == new_name


def test_customer_delete(client_api):
    customer = CustomerFactory()

    url = reverse("favorites:customers-detail", [customer.id])
    response = client_api.delete(url)

    with pytest.raises(ObjectDoesNotExist):
        customer.refresh_from_db()

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_product_list(client_api):
    product = ProductFactory()
    url = reverse("favorites:products-list")
    response = client_api.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    product_result = response.data[0]
    assert str(product.product_id) == product_result["product_id"]
    assert isoparse(str(product.created_at)) == isoparse(product_result["created_at"])
    assert isoparse(str(product.updated_at)) == isoparse(product_result["updated_at"])


@pytest.mark.freeze_time("2020-12-07")
@mock.patch("apps.favorites.serializers.ProductSerializer.check_product_existence")
def test_product_create(check_product_mock, client_api):
    product_payload = {"product_id": "08e79fe7-3957-4a7c-b423-fd6ccebd9baf"}
    check_product_mock.return_value = product_payload["product_id"]

    url = reverse("favorites:products-list")
    response = client_api.post(url, product_payload)

    product_result = response.data
    assert response.status_code == status.HTTP_201_CREATED
    assert product_payload["product_id"] in product_result["product_id"]
    assert product_result["created_at"] == "2020-12-07T00:00:00Z"
    assert product_result["updated_at"] == "2020-12-07T00:00:00Z"
    check_product_mock.assert_called_once()
    assert str(check_product_mock.call_args[0][0]) == product_payload["product_id"]


def test_product_delete(client_api):
    product = ProductFactory()

    url = reverse("favorites:products-detail", [product.product_id])
    response = client_api.delete(url)

    with pytest.raises(ObjectDoesNotExist):
        product.refresh_from_db()

    assert response.status_code == status.HTTP_204_NO_CONTENT


@mock.patch("apps.favorites.api.FavoriteViewSet.search_product")
def test_favorite_list(search_product_mock, luizalabs_product, client_api):
    customer = CustomerFactory()
    product = ProductFactory()
    customer.favorites.add(product)

    search_product_mock.return_value = luizalabs_product

    url = reverse("favorites:customer-favorites-list", [customer.id])
    response = client_api.get(url)

    assert response.status_code == status.HTTP_200_OK
    search_product_mock.assert_called_once()
    assert str(search_product_mock.call_args[0][0]) == product.product_id

    favorite_response = response.data[0]
    assert luizalabs_product["id"] == favorite_response["id"]
    assert float(luizalabs_product["price"]) == float(favorite_response["price"])
    assert luizalabs_product["image"] == favorite_response["image"]
    assert luizalabs_product["brand"] == favorite_response["brand"]
    assert luizalabs_product["title"] == favorite_response["title"]


def test_favorite_create(client_api):
    customer = CustomerFactory()
    product = ProductFactory()

    payload = {"product_id": str(product.product_id)}

    url = reverse("favorites:customer-favorites-list", [customer.id])
    response = client_api.post(url, payload)
    assert response.status_code == status.HTTP_201_CREATED

    customer.refresh_from_db()
    assert str(customer.favorites.first().product_id) == product.product_id


def test_favorite_create_already_created_favorite(client_api):
    customer = CustomerFactory()
    product = ProductFactory()
    customer.favorites.add(product)

    payload = {"product_id": str(product.product_id)}

    url = reverse("favorites:customer-favorites-list", [customer.id])
    response = client_api.post(url, payload)
    assert response.status_code == status.HTTP_304_NOT_MODIFIED


def test_favorite_create_invalid_product(client_api):
    customer = CustomerFactory()

    payload = {"product_id": uuid4()}

    url = reverse("favorites:customer-favorites-list", [customer.id])
    response = client_api.post(url, payload)

    expected_response = {"product_id": ["Given product_id does not exists"]}

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == expected_response


def test_favorite_destroy(client_api):
    customer = CustomerFactory()
    product = ProductFactory()
    customer.favorites.add(product)

    url = reverse("favorites:customer-favorites-detail", [customer.id, product.product_id])
    response = client_api.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    customer.refresh_from_db()
    assert customer.favorites.count() == 0


def test_favorite_destroy_already_destroyed_favorite(client_api):
    customer = CustomerFactory()
    product = ProductFactory()

    url = reverse("favorites:customer-favorites-detail", [customer.id, product.product_id])
    response = client_api.delete(url)
    assert response.status_code == status.HTTP_304_NOT_MODIFIED


def test_favorite_destroy_invalid_product(client_api):
    customer = CustomerFactory()

    url = reverse("favorites:customer-favorites-detail", [customer.id, uuid4()])
    response = client_api.delete(url)
    expected_response = {"product_id": ["Given product_id does not exists"]}

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == expected_response


@mock.patch("apps.favorites.api.FavoriteViewSet.search_product")
def test_favorite_retrieve(search_product_mock, luizalabs_product, client_api):
    customer = CustomerFactory()
    product = ProductFactory()
    customer.favorites.add(product)
    search_product_mock.return_value = luizalabs_product

    url = reverse("favorites:customer-favorites-detail", [customer.id, product.product_id])
    response = client_api.get(url)
    assert response.status_code == status.HTTP_200_OK

    assert response.status_code == status.HTTP_200_OK
    search_product_mock.assert_called_once()
    assert str(search_product_mock.call_args[0][0]) == product.product_id

    favorite_response = response.data
    assert luizalabs_product["id"] == favorite_response["id"]
    assert float(luizalabs_product["price"]) == float(favorite_response["price"])
    assert luizalabs_product["image"] == favorite_response["image"]
    assert luizalabs_product["brand"] == favorite_response["brand"]
    assert luizalabs_product["title"] == favorite_response["title"]
