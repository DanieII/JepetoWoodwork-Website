from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product


class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        return sum(
            float(product.product_total) for product in self.orderproduct_set.all()
        )


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    @property
    def product_total(self):
        return f"{self.product.price * self.quantity:.2f}"
