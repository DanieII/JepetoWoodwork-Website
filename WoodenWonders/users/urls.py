from django.urls import path
from users.views import UserRegisterView, UserLoginView, UserDetailsView

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("details/", UserDetailsView.as_view(), name="user_details"),
]
