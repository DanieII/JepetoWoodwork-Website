from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product
from phonenumber_field.modelfields import PhoneNumberField


class Order(models.Model):
    DELIVERY_CHOICES = [
        ("", "Delivery Type"),
        ("courier", "With Courier"),
        ("self_delivery", "Delivered by Us (for Sofia)"),
    ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    apartment_building = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.IntegerField()
    phone_number = PhoneNumberField()
    email = models.EmailField()
    delivery_type = models.CharField(
        max_length=100, choices=DELIVERY_CHOICES, default=""
    )
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
