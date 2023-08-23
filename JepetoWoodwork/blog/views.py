from django.views.generic import ListView, DetailView
from django.views.generic.base import reverse
from django.shortcuts import redirect
from .models import Blog, BlogComment
from .forms import BlogCommentForm
from users.mixins import HandleSendAndRetrieveLoginRequiredFormInformationMixin


class Blogs(ListView):
    model = Blog
    template_name = "blog/blog.html"


class BlogDetails(HandleSendAndRetrieveLoginRequiredFormInformationMixin, DetailView):
    model = Blog
    template_name = "blog/blog-details.html"
    mixin_form = BlogCommentForm
    fields = "__all__"
    success_message = "Коментарът е добавен"

    def get_success_url(self):
        return reverse("blog_details", kwargs={"slug": self.get_object().slug})

    def get_additional_fields(self):
        return {"user": self.request.user, "blog": self.get_object()}


def delete_comment_view(request, pk):
    comment = BlogComment.objects.get(pk=pk)

    if comment.user == request.user:
        comment.delete()

    blog_slug = comment.blog.slug
    blog_details_url = reverse("blog_details", kwargs={"slug": blog_slug})
    messages.success(request, "Коментарът е изтрит")

    return redirect(blog_details_url)
