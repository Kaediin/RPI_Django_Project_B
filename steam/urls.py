from django.urls import path

from steam.views import *


urlpatterns = [
    path("", homepage, name='homepage'),
    # path("/test_ajax/", ajax_view, name='ajax_test'),
    # path("Home/", homepage, name='homepage'),
    path("Logout/", logout, name='logout'),
    path('fetch_all_steam_data', fetch_steam_data_ajax, name='fetch_steam_apps'),
    path('Details/<appid>', app_details, name='open_app_details'),
    path('fetch_app_details/<appid>', fetch_details_ajax, name='fetch_details'),
    path('Servo/<percentage>', start_servo, name='set_percentage_servo')

]