from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Blog, BlogComment
from django.core.cache.utils import make_template_fragment_key


@receiver(post_save, sender=Blog)
@receiver(post_delete, sender=Blog)
def invalidate_blog_posts_cache(sender, instance, **kwargs):
    cache.delete(make_template_fragment_key("blog_posts"))


@receiver(post_save, sender=BlogComment)
@receiver(post_delete, sender=BlogComment)
def invalidate_blog_comments_cache(sender, instance, **kwargs):
    cache.delete(make_template_fragment_key("blog_posts"))
    cache.delete(make_template_fragment_key("blog_comments", [instance.blog.pk]))
