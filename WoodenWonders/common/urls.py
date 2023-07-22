from django.urls import path
from common.views import Home, Contacts

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("contacts/", Contacts.as_view(), name="contacts"),
]
