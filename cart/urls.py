from django.urls import path

from .views import (
    CheckoutView,
    add_to_cart_view,
    cart_view,
    decrease_quantity_view,
    remove_product_view,
)


urlpatterns = [
    path("", cart_view, name="cart"),
    path("add-to-cart/<slug:slug>/", add_to_cart_view, name="add_to_cart"),
    path(
        "decrease-quantity/<slug:slug>/",
        decrease_quantity_view,
        name="decrease_quantity",
    ),
    path("remove-product/<slug:slug>/", remove_product_view, name="remove_product"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
]
