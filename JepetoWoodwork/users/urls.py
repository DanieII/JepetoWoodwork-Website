from django.urls import path
from users.views import (
    UserRegisterView,
    UserLoginView,
    UserDetailsView,
    UserOrders,
    ChangePasswordView,
    logout_view,
)
from cart.views import (
    delete_saved_checkout_information_view,
    SavedCheckoutInformationView,
)


urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("details/", UserDetailsView.as_view(), name="user_details"),
    path("orders/", UserOrders.as_view(), name="user_orders"),
    path("logout/", logout_view, name="logout"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    path(
        "saved-checkout-information/",
        SavedCheckoutInformationView.as_view(),
        name="saved_checkout_information",
    ),
    path(
        "delete-saved-checkout-information/",
        delete_saved_checkout_information_view,
        name="delete_saved_checkout_information",
    ),
]
