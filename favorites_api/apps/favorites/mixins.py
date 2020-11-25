import requests
from django.core.cache import cache
from environs import Env
from rest_framework import status

env = Env()
env.read_env()


class ExternalLuizalabsAPIMixin:
    def store_product_on_cache(self, id, data):
        cache.add(id, data, env.int("FAVORITES_EXPIRE_TIMEOUT"))

    def search_product_on_cache(self, id):
        return cache.get(id)

    def search_product_on_external_api(self, id):
        """
        Search given id on external LUIZALABS_API.
        The value returned from the API will be automatically stored on cache to avoid further requests.
        """
        luizalabs_api_url = env("LUIZALABS_API_URL")
        url = f"{luizalabs_api_url}/api/product/{id}/"

        response = requests.request("GET", url)

        data = response.json() if response.status_code == status.HTTP_200_OK else {}
        self.store_product_on_cache(id, data)
        return data

    def search_product(self, id):
        """
        Search for given id. This will first search on cache, then in case this info doesn't exist on cache
        it will search on external_api.
        """
        cache_value = self.search_product_on_cache(id)
        if cache_value is None:
            return self.search_product_on_external_api(id)
        return cache_value

    def check_product_existence(self, id):
        return self.search_product(id) != {}
