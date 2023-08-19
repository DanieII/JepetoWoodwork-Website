from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product
from phonenumber_field.modelfields import PhoneNumberField
from common.validators import only_letters_validator

UserModel = get_user_model()


class Order(models.Model):
    DELIVERY_CHOICES = [
        ("", "Вид доставка"),
        ("courier", "С куриер: 7.00 лв."),
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
    phone_number = PhoneNumberField(verbose_name="Телефонен номер")
    email = models.EmailField(verbose_name="Имейл")
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


class SavedCheckoutInformation(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
