from unittest import mock

import pytest
import responses
from django.test import override_settings
from rest_framework import status

from apps.core.mixins import ExternalLuizalabsAPIMixin


@pytest.fixture
def external_luizalabs_api_mixin():
    return ExternalLuizalabsAPIMixin()


@mock.patch("apps.core.mixins.cache")
@override_settings(FAVORITES_EXPIRE_TIMEOUT=10)
def test_external_luizalabs_store_empty_product(cache_mock, external_luizalabs_api_mixin, id):
    timeout = 10

    external_luizalabs_api_mixin.store_product_on_cache(id, {})
    cache_mock.add.assert_called_once_with(id, {}, timeout)


@mock.patch("apps.core.mixins.cache")
@override_settings(FAVORITES_EXPIRE_TIMEOUT=10)
def test_external_luizalabs_store_product(cache_mock, external_luizalabs_api_mixin, id, luizalabs_product):
    timeout = 10

    external_luizalabs_api_mixin.store_product_on_cache(id, luizalabs_product)
    cache_mock.add.assert_called_once_with(id, luizalabs_product, timeout)


@mock.patch("apps.core.mixins.cache")
def test_external_luizalabs_search_product_on_cache(
    cache_mock, external_luizalabs_api_mixin, id, luizalabs_product
):
    cache_mock.get.return_value = luizalabs_product

    assert external_luizalabs_api_mixin.search_product_on_cache(id) == luizalabs_product
    cache_mock.get.assert_called_once_with(id)


@responses.activate
@mock.patch("apps.core.mixins.ExternalLuizalabsAPIMixin.store_product_on_cache")
@override_settings(LUIZALABS_API_URL="http://local-challenge-api.luizalabs.com")
def test_external_luizalabs_search_product_on_external_api(
    store_product_mock, external_luizalabs_api_mixin, id, luizalabs_product
):
    url = "http://local-challenge-api.luizalabs.com"

    expected_url = f"{url}/api/product/{id}/"
    responses.add(
        responses.GET,
        expected_url,
        status=status.HTTP_200_OK,
        json=luizalabs_product,
    )

    response = external_luizalabs_api_mixin.search_product_on_external_api(id)
    assert response == luizalabs_product
    store_product_mock.assert_called_once_with(id, luizalabs_product)


@responses.activate
@mock.patch("apps.core.mixins.ExternalLuizalabsAPIMixin.store_product_on_cache")
@override_settings(LUIZALABS_API_URL="http://local-challenge-api.luizalabs.com")
def test_external_luizalabs_search_invalid_product_on_external_api(
    store_product_mock, external_luizalabs_api_mixin, id
):
    url = "http://local-challenge-api.luizalabs.com"

    expected_response = {"error_message": f"Product {id} not found", "code": "not_found"}

    expected_url = f"{url}/api/product/{id}/"
    responses.add(
        responses.GET,
        expected_url,
        status=status.HTTP_404_NOT_FOUND,
        json=expected_response,
    )

    response = external_luizalabs_api_mixin.search_product_on_external_api(id)
    assert response == {}
    store_product_mock.assert_called_once_with(id, {})


@mock.patch("apps.core.mixins.ExternalLuizalabsAPIMixin.search_product_on_cache")
@mock.patch("apps.core.mixins.ExternalLuizalabsAPIMixin.search_product_on_external_api")
def test_external_luizalabs_search_product_exists_on_cache(
    search_external_api_mock, search_cache_mock, external_luizalabs_api_mixin, id, luizalabs_product
):
    search_cache_mock.return_value = luizalabs_product
    data = external_luizalabs_api_mixin.search_product(id)

    assert data == luizalabs_product
    search_cache_mock.assert_called_once_with(id)
    search_external_api_mock.assert_not_called()


@mock.patch("apps.core.mixins.ExternalLuizalabsAPIMixin.search_product_on_cache")
@mock.patch("apps.core.mixins.ExternalLuizalabsAPIMixin.search_product_on_external_api")
def test_external_luizalabs_search_product_exists_empty_on_cache(
    search_external_api_mock, search_cache_mock, external_luizalabs_api_mixin, id
):
    search_cache_mock.return_value = {}
    data = external_luizalabs_api_mixin.search_product(id)

    assert data == {}
    search_cache_mock.assert_called_once_with(id)
    search_external_api_mock.assert_not_called()


@mock.patch("apps.core.mixins.ExternalLuizalabsAPIMixin.search_product_on_cache")
@mock.patch("apps.core.mixins.ExternalLuizalabsAPIMixin.search_product_on_external_api")
def test_external_luizalabs_search_product_exists_on_api(
    search_external_api_mock, search_cache_mock, external_luizalabs_api_mixin, id, luizalabs_product
):
    search_cache_mock.return_value = None
    search_external_api_mock.return_value = luizalabs_product

    data = external_luizalabs_api_mixin.search_product(id)

    assert data == luizalabs_product
    search_cache_mock.assert_called_once_with(id)
    search_external_api_mock.assert_called_once_with(id)


@mock.patch("apps.core.mixins.ExternalLuizalabsAPIMixin.search_product_on_cache")
@mock.patch("apps.core.mixins.ExternalLuizalabsAPIMixin.search_product_on_external_api")
def test_external_luizalabs_search_product_do_not_exists_on_api(
    search_external_api_mock,
    search_cache_mock,
    external_luizalabs_api_mixin,
    id,
):
    search_cache_mock.return_value = None
    search_external_api_mock.return_value = {}

    data = external_luizalabs_api_mixin.search_product(id)

    assert data == {}
    search_cache_mock.assert_called_once_with(id)
    search_external_api_mock.assert_called_once_with(id)


@pytest.mark.parametrize(
    "search_output, expected_response",
    (
        ({}, False),
        ({"valid": "payload"}, True),
    ),
)
@mock.patch("apps.core.mixins.ExternalLuizalabsAPIMixin.search_product")
def test_external_luizalabs_check_product_existence(
    search_product_mock, search_output, expected_response, external_luizalabs_api_mixin, id
):
    search_product_mock.return_value = search_output

    assert external_luizalabs_api_mixin.check_product_existence(id) == expected_response
    search_product_mock.assert_called_once_with(id)
