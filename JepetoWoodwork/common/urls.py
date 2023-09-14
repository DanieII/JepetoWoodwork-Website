from django.urls import path
from common.views import (
    AboutUsView,
    FAQView,
    HomeView,
    ContactsView,
    PrivacyPolicyView,
    TermsOfUseView,
)
from django.views.decorators.cache import cache_page

urlpatterns = [
    path("", cache_page(60 * 60 * 24 * 7)(HomeView.as_view()), name="home"),
    path(
        "contacts/",
        cache_page(60 * 60 * 24 * 7)(ContactsView.as_view()),
        name="contacts",
    ),
    path(
        "about-us/",
        cache_page(60 * 60 * 24 * 7)(AboutUsView.as_view()),
        name="about_us",
    ),
    path(
        "privacy-policy/",
        cache_page(60 * 60 * 24 * 7)(PrivacyPolicyView.as_view()),
        name="privacy_policy",
    ),
    path(
        "terms-of-use/",
        cache_page(60 * 60 * 24 * 7)(TermsOfUseView.as_view()),
        name="terms_of_use",
    ),
    path("faq/", cache_page(60 * 60 * 24 * 7)(FAQView.as_view()), name="faq"),
]
