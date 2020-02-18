from django.urls import path

from .views import (
    logout_view,
    login_view
)

# app_name = 'account'

urlpatterns = [
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login')
]