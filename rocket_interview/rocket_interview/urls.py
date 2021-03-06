from products.views import CatalogSizeView, CatalogItemView, CartView, CartItemView, CheckoutView

"""rocket_interview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]

# products
urlpatterns += [
    path('catalog/size/', CatalogSizeView.as_view(), ),
    path('catalog/<str:id>/', CatalogItemView.as_view()),
    path('cart/', CartView.as_view()),
    path('cart/item/<str:id>/', CartItemView.as_view()),
    path('cart/checkout/', CheckoutView.as_view())
]
