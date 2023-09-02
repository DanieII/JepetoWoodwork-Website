from django.urls import path
from common.views import (
    AboutUsView,
    FAQView,
    HomeView,
    ContactsView,
    PrivacyPolicyView,
    TermsOfUseView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("about-us/", AboutUsView.as_view(), name="about_us"),
    path("privacy-policy/", PrivacyPolicyView.as_view(), name="privacy_policy"),
    path("terms-of-use/", TermsOfUseView.as_view(), name="terms_of_use"),
    path("faq/", FAQView.as_view(), name="faq"),
]
