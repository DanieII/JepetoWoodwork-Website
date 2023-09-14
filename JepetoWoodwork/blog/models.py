from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to="blog_images")
    created_on = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class BlogComment(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
