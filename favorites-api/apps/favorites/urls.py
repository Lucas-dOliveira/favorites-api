from django.conf.urls import include, re_path
from rest_framework_nested import routers

from . import api

app_name = "favorites"

router = routers.SimpleRouter()

router.register(r"customers", api.CustomerViewSet, basename="customers")
router.register(r"products", api.ProductViewSet, basename="products")

customer_router = routers.NestedSimpleRouter(router, r"customers", lookup="customer")
customer_router.register(r"favorites", api.FavoriteViewSet, basename="customer-favorites")


urlpatterns = [
    re_path(r"^", include(router.urls)),
    re_path(r"^", include(customer_router.urls)),
]
