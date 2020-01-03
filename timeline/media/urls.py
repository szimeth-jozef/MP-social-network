from django.urls import path, include

from .views import (
    home_view, 
    profile_view,
    post_view,
    edit_profile,
    follow_detail
)

from .api.urls import urlpatterns as apiurls

# app_name = 'media'

urlpatterns = [
    path('home/', home_view, name='home'),
    path('edit/', edit_profile, name='edit-profile'),
    path('<str:username>/', profile_view, name='profile'),
    path('<str:username>/<str:follow>', follow_detail, name='follow-detail'),
    path('api/', include(apiurls)),
    path('post/<slug:slug>/', post_view, name='post'),
   
] 