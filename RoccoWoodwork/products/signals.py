from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from .models import Product, ProductImage, Category, ProductReview


@receiver(post_delete, sender=Category)
@receiver(post_save, sender=Category)
def invalidate_categories_cache(sender, instance, **kwargs):
    cache.delete("categories")
    cache.delete("products")
    for product in instance.product_set.all():
        print(product.pk)
        cache.delete(make_template_fragment_key("product_details", [product.pk]))


@receiver(post_delete, sender=ProductReview)
@receiver(post_save, sender=ProductReview)
def invalidate_product_reviews_cache(sender, instance, **kwargs):
    cache_key = make_template_fragment_key("product_reviews", [instance.product.pk])
    cache.delete(cache_key)


@receiver(post_save, sender=Product)
@receiver(post_delete, sender=Product)
@receiver(post_delete, sender=ProductImage)
@receiver(post_save, sender=ProductImage)
def invalidate_product_cache(sender, instance, **kwargs):
    cache.delete("products")

    if isinstance(instance, Product):
        cache.delete(make_template_fragment_key("product_details", [instance.pk]))
    else:
        cache.delete(
            make_template_fragment_key("product_details", [instance.product.pk])
        )
