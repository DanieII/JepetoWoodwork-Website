from django.urls import path
from .views import WishListView, handle_heart_button

urlpatterns = [
    path("heart/<int:pk>/", handle_heart_button, name="heart"),
    path("wishlist/", WishListView.as_view(), name="wishlist"),
]
