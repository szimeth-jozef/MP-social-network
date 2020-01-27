from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q

from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from rest_framework.authtoken.models import Token
from media.models import StatusPost
from account.models import Account
from comments.models import Comment
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
        'users': []
    }
    queryset = getUsers(keyword)

    for user in queryset:
        response['users'].append({
            'username': user.username,
            'fullName': user.full_name
        })

    return Response(response, content_type='application/json')


@api_view(["DELETE"])
def deletePost(request, slug):
    try:
        post = StatusPost.objects.get(slug=slug)
    except StatusPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    operation = post.delete()
    response = {}
    if operation:
        response["success"] = True
    else:
        response["success"] = False
    
    return Response(response, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def addComment(request):
    body = json.loads(request.body)
    commentWriter = request.user.username
    commentText = body['text']
    slug = body['slug']

    user = Account.objects.get(username=commentWriter)
    post = StatusPost.objects.get(slug=slug)

    comment = Comment.objects.create(user=user, post=post, text=commentText)
    return Response(status=status.HTTP_200_OK)

def getUsers(keyword):
    queryset = None
    queries = keyword.split(" ")
    for q in queries:
        users = Account.objects.filter(
            Q(username__icontains=q) |
            Q(full_name__icontains=q)
        ).distinct()

        queryset = [user for user in users]

    return list(set(queryset))

