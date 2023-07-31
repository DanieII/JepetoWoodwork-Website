from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from .models import Blog
from .forms import BlogCommentForm


class Blogs(ListView):
    model = Blog
    template_name = "blog/blog.html"


class BlogDetails(FormMixin, DetailView):
    model = Blog
    template_name = "blog/blog-details.html"
    form_class = BlogCommentForm
