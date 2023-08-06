from django.urls import path
from products.views import Products, ProductDetails

urlpatterns = [
    path("", Products.as_view(), name="products"),
    path("details/<slug>/", ProductDetails.as_view(), name="product_details"),
]
