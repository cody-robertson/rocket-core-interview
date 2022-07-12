from django.db.models import Count, Sum
from rest_framework.views import APIView, Response
from rest_framework import serializers
from .models import Product, Cart
from .serializers import ProductSerializer, ProductInCartSerializer
import logging


logger = logging.getLogger(__name__)


class Status:
    def __init__(self, success: bool):
        super().__init__()
        self.success = success


class CountObject(Status):
    def __init__(self, count: int, success: bool):
        super().__init__(success)
        self.count = count


class Products(Status):
    def __init__(self, products: list[Product], success: bool):
        super().__init__(success)
        self.products = products


class ProductsAndTotal(Products):
    def __init__(self, total_cost: int, products: list[Product], success: bool):
        super().__init__(products, success)
        self.total_cost = total_cost


class StatusResponse(serializers.Serializer):
    success = serializers.BooleanField()


class CountResponse(StatusResponse):
    count = serializers.IntegerField()


class ProductsSerializer(StatusResponse):
    products = serializers.ListSerializer(child=ProductSerializer())


class ProductsInCartSerializer(StatusResponse):
    products = serializers.ListSerializer(child=ProductInCartSerializer())


class ProductsAndTotalSerializer(ProductsInCartSerializer):
    total_cost = serializers.IntegerField()


def error_wrapper(fun):
    def inner_wrapper(*args, **kwargs):
        try:
            return fun(*args, **kwargs)
        except Exception as e:
            logger.exception(e)
            return Response(data=StatusResponse(Status(False)).data, status=501)
    return inner_wrapper


class CatalogSizeView(APIView):
    @error_wrapper
    def get(self, request):
        """
        Gets the total number of products
        """
        count = Product.objects.count()
        response = CountResponse(CountObject(count=count, success=True))
        return Response(data=response.data, status=200)


class CatalogItemView(APIView):
    @error_wrapper
    def get(self, request, id: str):
        """
        Gets a single product by id
        """
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response(data=StatusResponse(Status(False)).data, status=404)

        response = ProductsSerializer(Products(products=[product], success=True))
        return Response(data=response.data, status=200)


class CartView(APIView):
    @error_wrapper
    def get(self, request):
        """
        Gets current products in cart and total cost
        """
        cart = Cart.objects.get()
        products = cart.products.all()
        total_cost = products.aggregate(sum=Sum('price'))['sum'] or 0

        response = ProductsAndTotalSerializer(ProductsAndTotal(success=True, products=products, total_cost=total_cost))
        return Response(data=response.data, status=200)


class CartItemView(APIView):
    failure_response = Response(StatusResponse(Status(success=False)).data, status=404)

    @error_wrapper
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

        response = ProductsInCartSerializer(Products(products=[product], success=True))
        return Response(data=response.data, status=200)

    @error_wrapper
    def post(self, request, id: str):
        """
        Adds a product to the cart and updates quantity
        """
        try:
            product = Product.available.get(id=id)
        except Product.DoesNotExist:
            return Response(data=self.failure_response.data, status=404)

        if product.cart:
            return Response(data=self.failure_response.data, status=501)

        cart = Cart.objects.get()
        product.cart = cart
        product.quantity = 0
        product.save()

        response = StatusResponse(Status(success=True))
        return Response(data=response.data, status=200)

    @error_wrapper
    def delete(self, request, id: str):
        """
        Removes an item from the cart and updates quantity
        """
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response(data=self.failure_response.data, status=404)

        if product.cart is None:
            return Response(data=self.failure_response.data, status=404)

        product.cart = None
        product.quantity = 1
        product.save()

        response = StatusResponse(Status(success=True))
        return Response(data=response.data, status=200)


class CheckoutView(APIView):
    @error_wrapper
    def post(self, request):
        """
        Clears the cart and returns the previous value of the cart
        """
        cart = Cart.objects.get()
        products = list(cart.products.all())
        total_cost = cart.products.aggregate(sum=Sum('price'))['sum']

        if not len(products):
            return Response(data=StatusResponse(Status(success=False)).data, status=501)

        response_data = ProductsAndTotalSerializer(ProductsAndTotal(products=products, total_cost=total_cost, success=True)).data

        # assumption is to keep products at their reduced quantity
        # therefore, no need to update quantity further on checkout
        cart.products.set([])
        cart.save()

        return Response(data=response_data, status=200)

