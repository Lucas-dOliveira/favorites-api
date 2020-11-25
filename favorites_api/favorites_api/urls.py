from django.conf.urls import include, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    re_path(r"^v1/", include("apps.favorites.urls", namespace="favorites")),
    re_path(r"^v1/auth/", TokenObtainPairView.as_view(), name="token_obtain_pair_view"),
    re_path(r"^v1/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
