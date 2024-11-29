from django.db import models
from products.models import Product
from phonenumber_field.modelfields import PhoneNumberField
from common.validators import only_alpha
import uuid


class Order(models.Model):
    first_name = models.CharField(
        max_length=100, validators=[only_alpha], verbose_name="Име"
    )
    last_name = models.CharField(
        max_length=100, validators=[only_alpha], verbose_name="Фамилия"
    )
    city = models.CharField(
        max_length=100, validators=[only_alpha], verbose_name="Град"
    )
    address = models.CharField(max_length=100, verbose_name="Адрес")
    email = models.EmailField(verbose_name="Имейл")
    phone_number = PhoneNumberField(
        verbose_name="Телефонен номер",
        error_messages={"invalid": "Въведете валиден телефонен номер"},
    )
    number = models.UUIDField(
        blank=True, default=uuid.uuid4, verbose_name="Номер на поръчката"
    )
    created_on = models.DateTimeField(auto_now=True, verbose_name="Създадена на")

    @property
    def total_price(self):
        products_price_sum = sum(
            product.total_price for product in self.orderproduct_set.all()
        )

        return products_price_sum

    class Meta:
        verbose_name = "Поръчка"
        verbose_name_plural = "Поръчки"


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Продукт"
    )
    quantity = models.IntegerField(verbose_name="Количество")

    @property
    def total_price(self):
        return self.product.price * self.quantity
