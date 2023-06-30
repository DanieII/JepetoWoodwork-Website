from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models


class Product(models.Model):
    name = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(5)
        ]
    )
    price = models.FloatField(
        validators=[
            MinValueValidator(0)
        ]
    )
    categories = models.ManyToManyField(
        to='Category'
    )
    image = models.ImageField(upload_to='product_images/')
    quantity = models.PositiveIntegerField()
    description = models.TextField(
        null=True,
        blank=True
    )
    slug = models.SlugField(
        unique=True
    )
    date_added = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=200
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
