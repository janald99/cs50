import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post


def index(request, postpage=None):
    if postpage == "following":
        posts = Post.objects.filter(user__in=request.user.following.all()).order_by('-timestamp')
        can_post = False
    else:
        # all posts
        posts = Post.objects.all().order_by('-timestamp')
        can_post = True

    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    liked_post_ids = []
    if request.user.is_authenticated:
        liked_post_ids = Post.objects.filter(likes=request.user).values_list('id', flat=True)

    return render(request, "network/index.html", {"posts": posts, "user": request.user, "page_obj": page_obj, "liked_post_ids": liked_post_ids, "can_post" : can_post})


@login_required
def following(request):
    following_posts = Post.objects.filter(user__in=request.user.following.all()).order_by('-timestamp')
    paginator = Paginator(following_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {"following_posts": following_posts, "page_obj": page_obj})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def new_post(request):
    if request.method == "POST":
        post_content = request.POST.get("post_content")
        # Create a new post and save it to the database
        new_post = Post(user=request.user, content=post_content)
        new_post.save()
        return HttpResponseRedirect(reverse("index"))  # Redirect to the same page after posting.
    else:
        # Handle GET requests, if necessary
        return render(request, "network/index.html", {
            "posts": Post.objects.all().order_by('-timestamp')
        })
    
@login_required
def edit_post(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    post_id = data.get("post_id")
    edited_content = data.get("content")

    post = Post.objects.get(id=post_id)

    post.content = edited_content
    post.save()

    return JsonResponse({"success": True})

@login_required
def like_post(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required.'}, status=400)

    data = json.loads(request.body)
    post_id = data.get('post_id')
    action = data.get('action')

    post = Post.objects.get(id=post_id)

    if action == 'like':
        post.likes.add(request.user)
    elif action == 'unlike':
        post.likes.remove(request.user)
    else:
        return JsonResponse({'error': 'Invalid action.'}, status=400)

    post.save()

    return JsonResponse({'success': True, 'like_count': post.likes.count()})

def profile(request, username):
    try:
        user_profile = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse("User not found", status=404)

    is_self = False
    is_following = False

    if request.user.is_authenticated:
        # Check if the logged-in user is viewing their own profile
        is_self = user_profile == request.user

        # Check if the logged-in user is following this user
        if not is_self:
            is_following = user_profile.followers.filter(id=request.user.id).exists()

    # Retrieve the user's posts in reverse chronological order
    user_posts = Post.objects.filter(user=user_profile).order_by('-timestamp')

    return render(request, "network/profile.html", {
        "user_profile": user_profile,
        "is_self": is_self,
        "is_following": is_following,
        "user_posts": user_posts,
    })


@login_required
def follow_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    username = data.get("username")

    user_to_follow = User.objects.get(username=username)

    action = data.get("action")

    if action == "follow":
        user_to_follow.followers.add(request.user)
        request.user.following.add(user_to_follow) 
        request.user.save()
        user_to_follow.save()
        print(user_to_follow.followers)
        print(request.user.following)
        response_data = {
            "message": "User followed successfully.",
            "followersCount": user_to_follow.followers.count(),
            "followingCount": user_to_follow.following.count(),
        }
    elif action == "unfollow":
        user_to_follow.followers.remove(request.user)
        request.user.following.remove(user_to_follow)
        request.user.save()
        user_to_follow.save()
        print(request.user.following)
        response_data = {
            "message": "User unfollowed successfully.",
            "followersCount": user_to_follow.followers.count(),
            "followingCount": user_to_follow.following.count(),
        }
    else:
        response_data = {"message": "Invalid action."}

    return JsonResponse(response_data)