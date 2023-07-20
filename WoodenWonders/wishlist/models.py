from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product


class Wishlist(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
