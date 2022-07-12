from django.shortcuts import render
from rest_framework.views import APIView

# Create your views here.
class ProductsView(APIView):
    def get(self, request):
        """
        Return a list of all products
        """