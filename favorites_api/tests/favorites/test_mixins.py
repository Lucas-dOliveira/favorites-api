from unittest import mock

import pytest
import responses
from rest_framework import status

from apps.favorites.mixins import ExternalLuizalabsAPIMixin


@pytest.fixture
def external_luizalabs_api_mixin():
    return ExternalLuizalabsAPIMixin()


@mock.patch("apps.favorites.mixins.cache")
@mock.patch("apps.favorites.mixins.env")
def test_external_luizalabs_store_empty_product(
    env_mock, cache_mock, external_luizalabs_api_mixin, product_id
):
    timeout = 10
    env_mock.int.return_value = timeout

    external_luizalabs_api_mixin.store_product_on_cache(product_id, {})
    cache_mock.add.assert_called_once_with(product_id, {}, timeout)


@mock.patch("apps.favorites.mixins.cache")
@mock.patch("apps.favorites.mixins.env")
def test_external_luizalabs_store_product(
    env_mock, cache_mock, external_luizalabs_api_mixin, product_id, luizalabs_product
):
    timeout = 10
    env_mock.int.return_value = timeout

    external_luizalabs_api_mixin.store_product_on_cache(product_id, luizalabs_product)
    cache_mock.add.assert_called_once_with(product_id, luizalabs_product, timeout)


@mock.patch("apps.favorites.mixins.cache")
def test_external_luizalabs_search_product_on_cache(
    cache_mock, external_luizalabs_api_mixin, product_id, luizalabs_product
):
    cache_mock.get.return_value = luizalabs_product

    assert external_luizalabs_api_mixin.search_product_on_cache(product_id) == luizalabs_product
    cache_mock.get.assert_called_once_with(product_id)


@responses.activate
@mock.patch("apps.favorites.mixins.env")
@mock.patch("apps.favorites.mixins.ExternalLuizalabsAPIMixin.store_product_on_cache")
def test_external_luizalabs_search_product_on_external_api(
    store_product_mock, env_mock, external_luizalabs_api_mixin, product_id, luizalabs_product
):
    url = "http://local-challenge-api.luizalabs.com"
    env_mock.return_value = url

    expected_url = f"{url}/api/product/{product_id}/"
    responses.add(
        responses.GET,
        expected_url,
        status=status.HTTP_200_OK,
        json=luizalabs_product,
    )

    response = external_luizalabs_api_mixin.search_product_on_external_api(product_id)
    assert response == luizalabs_product
    store_product_mock.assert_called_once_with(product_id, luizalabs_product)


@responses.activate
@mock.patch("apps.favorites.mixins.env")
@mock.patch("apps.favorites.mixins.ExternalLuizalabsAPIMixin.store_product_on_cache")
def test_external_luizalabs_search_invalid_product_on_external_api(
    store_product_mock, env_mock, external_luizalabs_api_mixin, product_id
):
    url = "http://local-challenge-api.luizalabs.com"
    env_mock.return_value = url

    expected_response = {"error_message": f"Product {product_id} not found", "code": "not_found"}

    expected_url = f"{url}/api/product/{product_id}/"
    responses.add(
        responses.GET,
        expected_url,
        status=status.HTTP_404_NOT_FOUND,
        json=expected_response,
    )

    response = external_luizalabs_api_mixin.search_product_on_external_api(product_id)
    assert response == {}
    store_product_mock.assert_called_once_with(product_id, {})


@mock.patch("apps.favorites.mixins.ExternalLuizalabsAPIMixin.search_product_on_cache")
@mock.patch("apps.favorites.mixins.ExternalLuizalabsAPIMixin.search_product_on_external_api")
def test_external_luizalabs_search_product_exists_on_cache(
    search_external_api_mock, search_cache_mock, external_luizalabs_api_mixin, product_id, luizalabs_product
):
    search_cache_mock.return_value = luizalabs_product
    data = external_luizalabs_api_mixin.search_product(product_id)

    assert data == luizalabs_product
    search_cache_mock.assert_called_once_with(product_id)
    search_external_api_mock.assert_not_called()


@mock.patch("apps.favorites.mixins.ExternalLuizalabsAPIMixin.search_product_on_cache")
@mock.patch("apps.favorites.mixins.ExternalLuizalabsAPIMixin.search_product_on_external_api")
def test_external_luizalabs_search_product_exists_empty_on_cache(
    search_external_api_mock, search_cache_mock, external_luizalabs_api_mixin, product_id
):
    search_cache_mock.return_value = {}
    data = external_luizalabs_api_mixin.search_product(product_id)

    assert data == {}
    search_cache_mock.assert_called_once_with(product_id)
    search_external_api_mock.assert_not_called()


@mock.patch("apps.favorites.mixins.ExternalLuizalabsAPIMixin.search_product_on_cache")
@mock.patch("apps.favorites.mixins.ExternalLuizalabsAPIMixin.search_product_on_external_api")
def test_external_luizalabs_search_product_exists_on_api(
    search_external_api_mock, search_cache_mock, external_luizalabs_api_mixin, product_id, luizalabs_product
):
    search_cache_mock.return_value = None
    search_external_api_mock.return_value = luizalabs_product

    data = external_luizalabs_api_mixin.search_product(product_id)

    assert data == luizalabs_product
    search_cache_mock.assert_called_once_with(product_id)
    search_external_api_mock.assert_called_once_with(product_id)


@mock.patch("apps.favorites.mixins.ExternalLuizalabsAPIMixin.search_product_on_cache")
@mock.patch("apps.favorites.mixins.ExternalLuizalabsAPIMixin.search_product_on_external_api")
def test_external_luizalabs_search_product_do_not_exists_on_api(
    search_external_api_mock,
    search_cache_mock,
    external_luizalabs_api_mixin,
    product_id,
):
    search_cache_mock.return_value = None
    search_external_api_mock.return_value = {}

    data = external_luizalabs_api_mixin.search_product(product_id)

    assert data == {}
    search_cache_mock.assert_called_once_with(product_id)
    search_external_api_mock.assert_called_once_with(product_id)


@pytest.mark.parametrize(
    "search_output, expected_response",
    (
        ({}, False),
        ({"valid": "payload"}, True),
    ),
)
@mock.patch("apps.favorites.mixins.ExternalLuizalabsAPIMixin.search_product")
def test_external_luizalabs_check_product_existence(
    search_product_mock, search_output, expected_response, external_luizalabs_api_mixin, product_id
):
    search_product_mock.return_value = search_output

    assert external_luizalabs_api_mixin.check_product_existence(product_id) == expected_response
    search_product_mock.assert_called_once_with(product_id)
