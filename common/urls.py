from django.urls import path
from common.views import (
    FAQView,
    HomeView,
    ContactsView,
    PrivacyPolicyView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path(
        "contacts/",
        ContactsView.as_view(),
        name="contacts",
    ),
    path(
        "privacy-policy/",
        PrivacyPolicyView.as_view(),
        name="privacy_policy",
    ),
    path("faq/", FAQView.as_view(), name="faq"),
]
