from rest_framework import serializers
from .models import Cart, Product


class ProductSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'quantity']

    def get_price(self, instance: Product):
        return int(instance.price)


class ProductInCartSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price']

    def get_price(self, instance: Product):
        return int(instance.price)
