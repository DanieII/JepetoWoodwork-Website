from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product
from phonenumber_field.modelfields import PhoneNumberField
from common.validators import only_alpha
import uuid

UserModel = get_user_model()


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
    notes = models.TextField(
        verbose_name="Бележки към поръчката (по избор)",
        null=True,
        blank=True,
    )
    number = models.CharField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        products_sum = sum(
            float(product.total_price) for product in self.orderproduct_set.all()
        )

        return products_sum

    def save(self):
        if not self.number:
            self.number = uuid.uuid4().hex[:5]

        return super().save()

    class Meta:
        verbose_name = "Поръчка"
        verbose_name_plural = "Поръчки"


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    @property
    def total_price(self):
        return f"{self.product.price * self.quantity:.2f}"
