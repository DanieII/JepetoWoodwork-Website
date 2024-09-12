from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product
from phonenumber_field.modelfields import PhoneNumberField
from common.validators import only_letters_validator
import uuid

UserModel = get_user_model()


class Order(models.Model):
    DELIVERY_CHOICES = [
        ("", "Вид доставка"),
        ("courier", "С куриер (За сметка на клиента)"),
        ("self_delivery", "Лично предаване (за гр. София)"),
    ]

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    first_name = models.CharField(
        max_length=100, validators=[only_letters_validator], verbose_name="Име"
    )
    last_name = models.CharField(
        max_length=100, validators=[only_letters_validator], verbose_name="Фамилия"
    )
    city = models.CharField(
        max_length=100, validators=[only_letters_validator], verbose_name="Град"
    )
    address = models.CharField(max_length=100, verbose_name="Адрес")
    apartment_building = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Апартамент, блок и т.н",
    )
    postal_code = models.IntegerField(verbose_name="Пощенски код")
    phone_number = PhoneNumberField(
        verbose_name="Телефонен номер",
        error_messages={"invalid": "Въведете валиден телефонен номер"},
    )
    email = models.EmailField(verbose_name="Имейл")
    delivery_type = models.CharField(
        max_length=100, choices=DELIVERY_CHOICES, default=""
    )
    notes = models.TextField(
        verbose_name="Бележки към поръчката (относно доставката или друго)",
        null=True,
        blank=True,
    )
    created_on = models.DateTimeField(auto_now=True)
    number = models.CharField(null=True, blank=True)

    def save(self):
        if not self.number:
            self.number = uuid.uuid4().hex[:5]
        return super().save()

    @property
    def total_price(self):
        products_sum = sum(
            float(product.product_total) for product in self.orderproduct_set.all()
        )

        return products_sum


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    @property
    def product_total(self):
        return f"{self.product.price * self.quantity:.2f}"


class SavedCheckoutInformation(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, validators=[only_letters_validator])
    last_name = models.CharField(max_length=100, validators=[only_letters_validator])
    city = models.CharField(max_length=100, validators=[only_letters_validator])
    address = models.CharField(max_length=100)
    apartment_building = models.CharField(
        max_length=100,
        null=True,
    )
    postal_code = models.IntegerField()
    phone_number = PhoneNumberField()
    email = models.EmailField()
    delivery_type = models.CharField(max_length=100)
