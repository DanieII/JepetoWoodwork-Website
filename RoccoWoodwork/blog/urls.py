from django.urls import path
from .views import Blogs, BlogDetails, delete_comment_view

urlpatterns = [
    path("", Blogs.as_view(), name="blog"),
    path(
        "details/<slug>/",
        BlogDetails.as_view(),
        name="blog_details",
    ),
    path("comment/delete/<int:pk>", delete_comment_view, name="delete_comment"),
]
