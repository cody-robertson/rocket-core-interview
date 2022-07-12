from rest_framework import serializers
from .models import Cart, Product


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'quantity']

    def get_price(self, instance: Product):
        return int(instance.price)


class CartSerializer(serializers.HyperlinkedModelSerializer):
    products = ProductSerializer(source="cart.products")

    class Meta:
        model = Cart
        fields = ['products']
