from django.urls import path

from .views import (
    makeFollow,
    likePost,
    searchUsers,
    deletePost,
    addComment,
)

urlpatterns = [
    path('makefollow/', makeFollow, name="makeFollow"),
    path('like/', likePost, name="likePost"),
    path('createComment/', addComment, name='addComment'),
    path('delete/<slug:slug>/', deletePost, name="deletePost"),
    path('<str:keyword>/', searchUsers, name='searchUsers'),
]