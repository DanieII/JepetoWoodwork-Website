from django.urls import path
from .views import (
    CheckoutView,
    add_to_cart,
    cart,
    decrease_quantity,
    remove_product,
)


urlpatterns = [
    path("", cart, name="cart"),
    path("add-to-cart/<slug>/", add_to_cart, name="add_to_cart"),
    path("decrease-quantity/<slug>/", decrease_quantity, name="decrease_quantity"),
    path("remove-product/<slug>/", remove_product, name="remove_product"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
]
