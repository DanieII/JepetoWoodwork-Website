from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from .models import Blog


@receiver(post_save, sender=Blog)
def invalidate_cache(sender, instance, **kwargs):
    cache.clear()
