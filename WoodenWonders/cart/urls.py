from django.urls import path
from .views import (
    CheckoutView,
    OrderSuccessView,
    add_to_cart,
    cart,
    decrease_quantity,
    increase_quantity,
    remove_product,
)

urlpatterns = [
    path("", cart, name="cart"),
    path("add-to-cart/<pk>/", add_to_cart, name="add_to_cart"),
    path("increase-quantity/<pk>/", increase_quantity, name="increase_quantity"),
    path("decrease-quantity/<pk>/", decrease_quantity, name="decrease_quantity"),
    path("remove-product/<pk>/", remove_product, name="remove_product"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("success/", OrderSuccessView.as_view(), name="order_success"),
]
