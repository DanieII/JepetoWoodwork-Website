from django.views.generic import ListView, DetailView
from django.views.generic.base import reverse
from .models import Blog
from .forms import BlogCommentForm
from users.mixins import HandleSendLoginRequiredFormInformationMixin


class Blogs(ListView):
    model = Blog
    template_name = "blog/blog.html"


class BlogDetails(HandleSendLoginRequiredFormInformationMixin, DetailView):
    model = Blog
    template_name = "blog/blog-details.html"
    mixin_form = BlogCommentForm
    fields = "__all__"

    def get_success_url(self):
        return reverse("blog_details", kwargs={"slug": self.get_object().slug})

    def get_additional_fields(self):
        return {"user": self.request.user, "blog": self.get_object()}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        comment = self.request.GET.get("comment")

        context["comment_form"] = BlogCommentForm(initial={"comment": comment})

        return context
