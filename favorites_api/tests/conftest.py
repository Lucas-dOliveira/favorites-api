import pytest
from rest_framework.test import APIClient


@pytest.fixture
def id():
    return "1bf0f365-fbdd-4e21-9786-da459d78dd1f"


@pytest.fixture
def luizalabs_product(id):
    return {
        "price": 1699.0,
        "image": "http://challenge-api.luizalabs.com/images/1bf0f365-fbdd-4e21-9786-da459d78dd1f.jpg",
        "brand": "bébé confort",
        "id": id,
        "title": "Cadeira para Auto Iseos Bébé Confort Earth Brown",
    }


@pytest.fixture()
def client_api():
    client = APIClient()
    return client
