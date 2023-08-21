from django.urls import path
from products.views import (
    ProductsView,
    ProductDetailsView,
    ProductsCategoryView,
    delete_review_view,
)

urlpatterns = [
    path("", ProductsView.as_view(), name="products"),
    path("<category>", ProductsCategoryView.as_view(), name="products_category"),
    path("details/<slug:slug>/", ProductDetailsView.as_view(), name="product_details"),
    path("review/delete/<int:pk>", delete_review_view, name="delete_review"),
]
