import uuid

from django.db import models


# Create your models here.
class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)


class Product(models.Model):
    id = models.CharField(primary_key=True, max_length=64)
    name = models.CharField(max_length=256, null=False, blank=False)
    price = models.DecimalField(decimal_places=2, max_digits=15)
    quantity = models.IntegerField()
    cart = models.ForeignKey(to=Cart, on_delete=models.SET_NULL, related_name="products", null=True)
