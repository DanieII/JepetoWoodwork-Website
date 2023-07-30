from django.urls import path
from .views import Blog, BlogDetails

urlpatterns = [
    path("", Blog.as_view(), name="blog"),
    path("blog/<int:pk>/", BlogDetails.as_view(), name="blog_details"),
]
