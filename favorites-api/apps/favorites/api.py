from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from .models import Customer, Product
from .serializers import CustomerSerializer, FavoriteListSerializer, FavoriteSerializer, ProductSerializer
from apps.core.mixins import ExternalLuizalabsAPIMixin


class ProductViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class FavoriteViewSet(viewsets.ViewSet, ExternalLuizalabsAPIMixin):
    def get_object(self, customer_pk):
        return get_object_or_404(Customer, id=customer_pk)

    @swagger_auto_schema(responses={200: FavoriteListSerializer(many=True)})
    def list(self, request, customer_pk, *args, **kwargs):
        qs = self.get_object(customer_pk).favorites.all()
        products = [self.search_product(product.id) for product in qs]

        serializer_class = self.get_serializer_class(request)
        serializer = serializer_class(products, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: FavoriteListSerializer})
    def retrieve(self, request, customer_pk, pk, *args, **kwargs):
        favorite = self.get_object(customer_pk).favorites.get(id=pk)
        detailed_product = self.search_product(favorite.id)

        serializer_class = self.get_serializer_class(request)
        serializer = serializer_class(detailed_product, many=False)
        return Response(serializer.data)

    @swagger_auto_schema(responses={201: "", 304: ""}, request_body=FavoriteSerializer)
    def create(self, request, customer_pk, *args, **kwargs):
        serializer_class = self.get_serializer_class(request)

        favorite_serializer = serializer_class(data=request.data)
        favorite_serializer.is_valid(raise_exception=True)

        id = request.data.get("id")

        product = get_object_or_404(Product, id=id)

        customer = self.get_object(customer_pk)
        if not customer.favorites.filter(id=id).exists():
            customer.favorites.add(product)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_304_NOT_MODIFIED)

    @swagger_auto_schema(responses={204: "", 304: ""}, request_body=FavoriteSerializer)
    def destroy(self, request, customer_pk, pk, *args, **kwargs):
        serializer_class = self.get_serializer_class(request)

        favorite_serializer = serializer_class(data={"id": pk})
        favorite_serializer.is_valid(raise_exception=True)

        product = get_object_or_404(Product, id=pk)

        customer = self.get_object(customer_pk)
        if customer.favorites.filter(id=pk).exists():
            customer.favorites.remove(product)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_304_NOT_MODIFIED)

    def get_serializer_class(self, request):
        return FavoriteListSerializer if request.method == "GET" else FavoriteSerializer
