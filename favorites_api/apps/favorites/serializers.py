from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from .mixins import ExternalLuizalabsAPIMixin
from .models import Customer, Product


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = (
            "id",
            "name",
            "email",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class ProductSerializer(serializers.ModelSerializer, ExternalLuizalabsAPIMixin):
    def validate_product_id(self, product_id):
        if self.check_product_existence(product_id):
            return product_id
        raise serializers.ValidationError(
            f"The product_id {product_id} wasn't found at Luizalabs products API"
        )

    class Meta:
        model = Product
        fields = (
            "product_id",
            "created_at",
            "updated_at",
        )


class FavoriteSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()

    def validate_product_id(self, product_id):
        try:
            Product.objects.get(product_id=product_id)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Given product_id does not exists")
        else:
            return product_id


class FavoriteListSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    image = serializers.URLField()
    brand = serializers.CharField(max_length=100)
