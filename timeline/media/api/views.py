from django.shortcuts import render, redirect
from django.http import HttpResponse

from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.authtoken.models import Token
from account.models import Account
from media.models import StatusPost
import json


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def makeFollow(request):
    responseData = {}

    try:
        frame_body = json.loads(request.body) 
        user_email = request.user                     # Account.email
        followed_username = frame_body['followed']    # Account.username

        user = Account.objects.get(email=user_email)
        followed_user = Account.objects.get(username=followed_username)
        all_followers_of_user = user.following.all()

        if followed_user not in all_followers_of_user:
            user.following.add(followed_user)
            followed_user.followers.add(user)
            responseData['buttonText'] = 'Unfollow'
        else:
            user.following.remove(followed_user)
            followed_user.followers.remove(user)
            responseData['buttonText'] = 'Follow'

        responseData['followers'] = len(followed_user.followers.all())
        responseData['following'] = len(followed_user.following.all())

        return Response(responseData)
    except ValueError as e:
        return Response(e)



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def likePost(request):
    response = {}

    body = json.loads(request.body)
    state = body['state']
    slug = body['slug']

    token = request.META['HTTP_AUTHORIZATION'].split()[1]
    user = Account.objects.get(email=Token.objects.get(key=token).user)
    post = StatusPost.objects.get(slug=slug)
    
    if state:
        post.likes.remove(user)
        response['state'] = False
        response['count'] = len(post.likes.all())
    else:
        post.likes.add(user)
        response['state'] = True
        response['count'] = len(post.likes.all())

    return Response(response)


@api_view(["GET"])
def searchUsers(request, keyword):
    response = {
        "keyword": keyword
    }

    return Response(response, content_type='application/json')

    