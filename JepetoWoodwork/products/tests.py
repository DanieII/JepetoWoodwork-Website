from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from .models import Product, ProductReview, Category
from django.shortcuts import reverse
from django.contrib.sessions.middleware import SessionMiddleware


UserModel = get_user_model()


class ProductsViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            name="Test Product",
            price=10.0,
            quantity=5,
        )
        self.product.categories.add(self.category)
        self.url = reverse("products")

    def test_view_uses_correct_template(self):
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, 200)
        self.assertTemplateUsed(request, "products/products.html")

    def test_queryset_is_filtered_by_search_query(self):
        request = self.client.get(self.url, {"search_field": "Test"})
        self.assertIn(self.product, request.context_data["object_list"])

    def test_queryset_is_filtered_by_category(self):
        request = self.client.get(self.url, {"categories": [self.category.id]})
        self.assertIn(self.product, request.context_data["object_list"])

    def test_queryset_is_filtered_by_price_range(self):
        request = self.client.get(self.url, {"min_price": "5.0", "max_price": "15.0"})
        self.assertIn(self.product, request.context_data["object_list"])


class ProductReviewModelTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email="test@example.com", password="testpassword"
        )
        self.product = Product.objects.create(
            name="Test Product", price=10.0, quantity=10, slug="test-product"
        )

    def test_create_product_review(self):
        review = ProductReview.objects.create(
            user=self.user, product=self.product, stars=4, review="Great product!"
        )
        self.assertEqual(ProductReview.objects.count(), 1)
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.product, self.product)
        self.assertEqual(review.stars, 4)
        self.assertEqual(review.review, "Great product!")
