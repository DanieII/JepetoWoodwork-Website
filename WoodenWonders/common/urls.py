from django.urls import path

from common.views import Home

urlpatterns = [
    path('', Home.as_view(), name='home')
]
