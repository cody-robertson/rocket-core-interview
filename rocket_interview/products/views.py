from django.db.models import Count, Sum
from rest_framework.views import APIView, Response
from rest_framework import serializers
from models import Product, Cart
from serializers import ProductSerializer


class Status:
    def __init__(self, success: bool):
        super().__init__()
        self.success = success


class CountObject(Status):
    def __init__(self, count: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.count = count


class Products(Status):
    def __init__(self, products: list[Product], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.products = products


class ProductsAndTotal(Products):
    def __init__(self, total_cost: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.total_cost = total_cost


class StatusResponse(serializers.Serializer):
    success = serializers.BooleanField()


class CountResponse(StatusResponse):
    count = serializers.IntegerField()


class ProductsSerializer(StatusResponse):
    products = serializers.ListSerializer(child=ProductSerializer)


class ProductsAndTotalSerializer(ProductsSerializer):
    total_cost = serializers.IntegerField()


class CatalogSizeView(APIView):
    def get(self, request):
        """
        Gets the total number of products
        """
        count = Product.objects.count()
        response = CountResponse(CountObject(count=count, success=True))
        return Response(data=response.data, status=200)


class CatalogItemView(APIView):
    def get(self, request, id: str):
        """
        Gets a single product by id
        """
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response(data=StatusResponse(Status(True)).data, status=404)

        response = ProductsSerializer(Products(products=[product]), success=False).data
        return Response(data=response.data, status=200)


class CartView(APIView):
    def get(self, request):
        """
        Gets current products in cart and total cost
        """
        cart = Cart.objects.get()
        products = cart.products.all()
        total_cost = products.aggregate(sum=Sum('price'))['sum']

        response = ProductsAndTotalSerializer(ProductsAndTotal(success=True, products=products, total_cost=total_cost))
        return Response(data=response.data, status=200)


class CartItemView(APIView):
    failure_response = Response(StatusResponse(Status(success=False)).data, status=404)

    def get(self, request, id: str):
        """
        Gets an item from the cart by id
        """
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response(data=self.failure_response.data, status=404)

        if product.cart is None:
            return Response(data=self.failure_response.data, status=404)

        response = ProductsSerializer(Products(products=[product], success=True))
        return Response(data=response.data, status=200)

    def post(self, request, id: str):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response(data=self.failure_response.data, status=404)

        if product.cart:
            return Response(data=self.failure_response.data, status=501)

        cart = Cart.objects.get()
        product.cart = cart
        product.save()

        response = StatusResponse(Status(success=True))
        return Response(data=response.data, status=200)

    def delete(self, request, id: str):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response(data=self.failure_response.data, status=404)

        if product.cart is None:
            return Response(data=self.failure_response.data, status=404)

        product.cart = None
        product.save()

        response = StatusResponse(Status(success=True))
        return Response(data=response.data, status=200)


class CheckoutView(APIView):
    def post(self, request):
        """
        Clears the cart and returns the previous value of the cart
        """
        cart = Cart.objects.get()
        products = cart.products
        total_cost = products.aggregate(sum=Sum('price'))['sum']

        if not len(products):
            return Response(data=StatusResponse(Status(success=False)).data, status=501)

        response_data = ProductsAndTotalSerializer(ProductsAndTotal(products=products, total_cost=total_cost, success=True)).data

        cart.products = []
        cart.save()

        return Response(data=response_data, status=200)

