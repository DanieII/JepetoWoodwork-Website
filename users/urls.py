from django.urls import path
from users.views import (
    UserRegisterView,
    UserLoginView,
    UserDetailsView,
    UserOrders,
    ChangePasswordView,
    logout_view,
)


urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("details/", UserDetailsView.as_view(), name="user_details"),
    path("orders/", UserOrders.as_view(), name="user_orders"),
    path("logout/", logout_view, name="logout"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
]
