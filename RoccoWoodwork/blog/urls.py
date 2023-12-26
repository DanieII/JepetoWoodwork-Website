from django.urls import path
from .views import Blogs, BlogDetails, delete_comment_view
from django.views.decorators.cache import cache_page

urlpatterns = [
    path("", cache_page(60 * 60 * 24 * 7)(Blogs.as_view()), name="blog"),
    path(
        "details/<slug>/",
        BlogDetails.as_view(),
        name="blog_details",
    ),
    path("comment/delete/<int:pk>", delete_comment_view, name="delete_comment"),
]
