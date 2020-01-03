from django.urls import path

from .views import (
    registration_view,
    logout_view,
    login_view
)

# app_name = 'account'

urlpatterns = [
    path('registration/', registration_view,  name="registration"),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login')
]