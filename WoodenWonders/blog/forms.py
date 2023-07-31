from django import forms
from django.contrib.auth import get_user_model
from .models import BlogComment


UserModel = get_user_model()


class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ["comment"]
        widgets = {"comment": forms.Textarea(attrs={"placeholder": "Your comment"})}
