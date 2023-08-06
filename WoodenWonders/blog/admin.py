from django.contrib import admin
from .models import Blog
from django.contrib.admin.options import format_html


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ["title", "blog_image"]
    search_fields = ["title"]
    search_help_text = "title"

    @staticmethod
    def blog_image(blog):
        return format_html(
            f'<img src="{blog.image.url}" alt="{blog.title} mage" style="max-height: 100px; max-width: 100px;" />',
        )
