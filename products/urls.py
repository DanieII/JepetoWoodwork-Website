from django.urls import path
from products.views import (
    ProductsView,
    ProductDetailsView,
    ProductsCategoryView,
)

urlpatterns = [
    path("", ProductsView.as_view(), name="products"),
    path(
        "<slug:slug>",
        ProductsCategoryView.as_view(),
        name="products_category",
    ),
    path(
        "details/<slug:slug>",
        ProductDetailsView.as_view(),
        name="product_details",
    ),
]
