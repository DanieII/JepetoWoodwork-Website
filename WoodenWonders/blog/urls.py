from django.urls import path
from .views import Blogs, BlogDetails

urlpatterns = [
    path("", Blogs.as_view(), name="blog"),
    path("blog/<slug>/", BlogDetails.as_view(), name="blog_details"),
]
