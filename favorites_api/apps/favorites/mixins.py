import requests
from django.core.cache import cache
from environs import Env
from rest_framework import status

env = Env()
env.read_env()


class ExternalLuizalabsAPIMixin:
    def store_product_on_cache(self, product_id, data):
        cache.add(product_id, data, env.int("FAVORITES_EXPIRE_TIMEOUT"))

    def search_product_on_cache(self, product_id):
        return cache.get(product_id)

    def search_product_on_external_api(self, product_id):
        """
        Search given product_id on external LUIZALABS_API.
        The value returned from the API will be automatically stored on cache to avoid further requests.
        """
        luizalabs_api_url = env("LUIZALABS_API_URL")
        url = f"{luizalabs_api_url}/api/product/{product_id}/"

        response = requests.request("GET", url)

        data = response.json() if response.status_code == status.HTTP_200_OK else {}
        self.store_product_on_cache(product_id, data)
        return data

    def search_product(self, product_id):
        """
        Search for given product_id. This will first search on cache, then in case this info doesn't exist on cache
        it will search on external_api.
        """
        cache_value = self.search_product_on_cache(product_id)
        if cache_value is None:
            return self.search_product_on_external_api(product_id)
        return cache_value

    def check_product_existence(self, product_id):
        return self.search_product(product_id) != {}
