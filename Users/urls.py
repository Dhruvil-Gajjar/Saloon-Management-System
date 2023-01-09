from django.urls import path

from Users.views import *


urlpatterns = [
    path('', dashboard, name='dashboard'),
]
