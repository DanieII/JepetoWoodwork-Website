from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import Blog, BlogComment
from django.shortcuts import reverse
from django.utils.text import slugify

UserModel = get_user_model()


class BlogsViewTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(email="test@gmail.com", password="test")
        self.blog = Blog.objects.create(
            title="Blog", content="Content", image="static/images/no-image.jpg"
        )

    def get_blog_comment(self):
        blog_comment = BlogComment.objects.create(
            blog=self.blog, user=self.user, comment="Test"
        )
        return blog_comment

    def test_blogs_view_renders_correct_template(self):
        response = self.client.get(reverse("blog"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/blog.html")

    def test_blog_created_properly(self):
        self.assertEqual(self.blog.title, "Blog")
        self.assertEqual(self.blog.content, "Content")
        self.assertEqual(self.blog.image, "static/images/no-image.jpg")
        self.assertEqual(self.blog.slug, slugify(self.blog.title))

    def test_add_blog_comment(self):
        blog_comment = self.get_blog_comment()
        self.assertEqual(blog_comment.blog, self.blog)
        self.assertEqual(blog_comment.user, self.user)
        self.assertEqual(blog_comment.comment, "Test")

    def test_blog_details_renders_comments(self):
        blog_comment = self.get_blog_comment()

        url = reverse("blog_details", kwargs={"slug": blog_comment.blog.slug})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, blog_comment.comment)
