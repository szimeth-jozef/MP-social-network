from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponse, HttpResponseRedirect, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from media.forms import CreateStatusPostForm

from rest_framework.authtoken.models import Token
from comments.models import Comment
from media.models import StatusPost
from account.models import Account


@login_required()
def follow_detail(request, username, follow):
    urlUser = validateUser(username)
    if not urlUser:
        return HttpResponseNotFound("We're sorry, this user does not exist.")

    context = {}

    if follow == "following":
        context['state'] = "following"
        return render(request, 'media/follow_detail.html', context)
    elif follow == "followers":
        context['state'] = "followers"
        return render(request, 'media/follow_detail.html', context)
    else:
        return Http404


@login_required()
def edit_profile(request):
    context = {}
    return render(request, 'media/edit.html', context)


@login_required()
def home_view(request):
    context = {}
    user = request.user
    form = CreateStatusPostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        author = Account.objects.filter(email=user.email).first()
        obj.author = author
        obj.save()
        form = CreateStatusPostForm()
        return HttpResponseRedirect('/site/home/')

    posts = getPostsFor(user)

    context['form'] = form
    context['posts'] = enumerate(posts)
    context['token'] = Token.objects.get(user=request.user)
    context['comments'] = commentCount(posts)

    return render(request, 'media/home.html', context)


@login_required()
def profile_view(request, username):
    urlUser = validateUser(username)
    if not urlUser:
        return HttpResponseNotFound("We're sorry, this user does not exist.")

    posts = StatusPost.objects.filter(author=urlUser).order_by('-date_posted')

    context = {
        'user': urlUser,
        'username': username,
        'token': Token.objects.get(user=request.user),
        'following': len(urlUser.following.all()),
        'followers': len(urlUser.followers.all()),
        'posts': enumerate(posts),
        'post_count': len(posts),
        'comments': commentCount(posts)
    }

    try:
        request.user.following.get(username=username)
        context['isFollowing'] = True
    except ObjectDoesNotExist:
        context['isFollowing'] = False

    if urlUser.about:
        context['about'] = urlUser.about

    return render(request, 'media/profile.html', context)


@login_required()
def post_view(request, slug):
    print(slug)
    context = {
        "slug": slug
    }
    return render(request, 'media/post_page.html', context)


def getPostsFor(user):
    mainQuerySet = StatusPost.objects.filter(author=user)   # QuerySet with the current users post (we need a start query set and everyone is seeing their own post oala)
    followedUsers = user.following.all()

    for u in followedUsers:
        mainQuerySet = mainQuerySet | StatusPost.objects.filter(author=u)
    
    return mainQuerySet.order_by('-date_posted')


def commentCount(posts):
    list_of_values = []
    for post in posts:
        comments = Comment.objects.filter(post=post)
        list_of_values.append(len(comments))
    return list_of_values


def validateUser(username):
    try:
        userExists = Account.objects.get(username=username)
        return userExists
    except ObjectDoesNotExist:
        return None