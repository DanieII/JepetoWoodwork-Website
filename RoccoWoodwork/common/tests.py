from django.test import TestCase
from django.shortcuts import reverse
from django.utils import timezone
from products.models import Product
from common.views import Home


class HomeViewTest(TestCase):
    def setUp(self):
        for i in range(5):
            Product.objects.create(
                name=f"Product {i}",
                price=10.0 * (i + 1),
                quantity=i + 1,
                date_added=timezone.now(),
            )

    def test_home_view_renders_correct_template(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "common/home.html")

    def test_home_view_orders_newest_arrivals_correctly(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

        newest_arrivals = response.context["object_list"]
        expected_order = list(
            Product.objects.order_by("-date_added")[: Home.NEWEST_ARRIVALS_NUMBER]
        )
        self.assertEqual(list(newest_arrivals), expected_order)
