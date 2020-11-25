from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from .mixins import ExternalLuizalabsAPIMixin
from .models import Customer, Product
from .serializers import CustomerSerializer, FavoriteListSerializer, FavoriteSerializer, ProductSerializer


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

    def list(self, request, customer_pk, *args, **kwargs):
        qs = self.get_object(customer_pk).favorites.all()
        products = [self.search_product(product.product_id) for product in qs]

        serializer_class = self.get_serializer_class(request)
        serializer = serializer_class(products, many=True)
        return Response(serializer.data)

    def retrieve(self, request, customer_pk, pk, *args, **kwargs):
        favorite = self.get_object(customer_pk).favorites.get(product_id=pk)
        detailed_product = self.search_product(favorite.product_id)

        serializer_class = self.get_serializer_class(request)
        serializer = serializer_class(detailed_product, many=False)
        return Response(serializer.data)

    def create(self, request, customer_pk, *args, **kwargs):
        serializer_class = self.get_serializer_class(request)

        favorite_serializer = serializer_class(data=request.data)
        favorite_serializer.is_valid(raise_exception=True)

        product_id = request.data.get("product_id")

        product = get_object_or_404(Product, product_id=product_id)

        customer = self.get_object(customer_pk)
        if not customer.favorites.filter(product_id=product_id).exists():
            customer.favorites.add(product)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_304_NOT_MODIFIED)

    def destroy(self, request, customer_pk, pk, *args, **kwargs):
        serializer_class = self.get_serializer_class(request)

        favorite_serializer = serializer_class(data={"product_id": pk})
        favorite_serializer.is_valid(raise_exception=True)

        product = get_object_or_404(Product, product_id=pk)

        customer = self.get_object(customer_pk)
        if customer.favorites.filter(product_id=pk).exists():
            customer.favorites.remove(product)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_304_NOT_MODIFIED)

    def get_serializer_class(self, request):
        return FavoriteListSerializer if request.method == "GET" else FavoriteSerializer
