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
    def validate_id(self, id):
        if self.check_product_existence(id):
            return id
        raise serializers.ValidationError(f"The id {id} wasn't found at Luizalabs products API")

    class Meta:
        model = Product
        fields = (
            "id",
            "created_at",
            "updated_at",
        )


class FavoriteSerializer(serializers.Serializer):
    id = serializers.UUIDField()

    def validate_id(self, id):
        try:
            Product.objects.get(id=id)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Given id does not exists")
        else:
            return id


class FavoriteListSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    image = serializers.URLField()
    brand = serializers.CharField(max_length=100)
    reviewScore = serializers.FloatField(allow_null=True)
