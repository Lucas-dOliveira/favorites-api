import pytest

from apps.favorites.models import DetailedProduct


@pytest.fixture
def product_id():
    return "1bf0f365-fbdd-4e21-9786-da459d78dd1f"


@pytest.fixture
def luizalabs_product(product_id):
    return {
        "price": 1699.0,
        "image": "http://challenge-api.luizalabs.com/images/1bf0f365-fbdd-4e21-9786-da459d78dd1f.jpg",
        "brand": "bébé confort",
        "id": product_id,
        "title": "Cadeira para Auto Iseos Bébé Confort Earth Brown",
    }


@pytest.fixture
def detailed_product(luizalabs_product):
    return DetailedProduct(**luizalabs_product)
