from django.urls import path

from .views import (
    makeFollow,
    likePost,
    searchUsers,
)

urlpatterns = [
    path('makefollow/', makeFollow, name="makeFollow"),
    path('like/', likePost, name="likePost"),
    path('<str:keyword>/', searchUsers, name='searchUsers')
]