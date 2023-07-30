from django.views.generic import ListView, DetailView
from .models import Blog


class Blog(ListView):
    model = Blog
    template_name = "blog/blog.html"


class BlogDetails(DetailView):
    model = Blog
    template_name = "blog/blog-details.html"
