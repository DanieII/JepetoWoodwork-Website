from django.urls import path

from common.views import Home, BaseTest

urlpatterns = [
    # path('', Home.as_view(), name='home')
    path('', BaseTest.as_view(), name='home')
]
