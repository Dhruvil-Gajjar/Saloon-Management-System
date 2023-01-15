from django.urls import path

from Shop.views import *


urlpatterns = [
    path('', landing_page, name='landing-page'),
]
