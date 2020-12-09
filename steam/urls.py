from django.urls import path

from steam.views import *


urlpatterns = [
    path("", index),
    path("/test_ajax/", ajax_view, name='ajax_test'),
    path("Home/", homepage, name='homepage'),
    path("Logout/", logout, name='logout')
]