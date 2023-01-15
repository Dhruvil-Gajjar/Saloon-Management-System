from django.urls import path

from Users.views import *


urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    
    path('sign-in/', sign_in, name='sign-in'),
    path('sign-up/', sign_up, name='sign-up'),
    
    path('sign-up-email/', sign_up_with_email, name='sign-up-email'),
    path('verify-email/<str:e_mail>/', verify_email, name='verify-email'),
    
    path('sign-up-number/', sign_up_with_number, name='sign-up-number'),
    path('verify-number/<str:phone_number>/', verify_number, name='verify-number'),
]

