from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post


def index(request):
    posts = Post.objects.all().order_by('-timestamp')
    return render(request, "network/index.html", {"posts": posts})


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
    
def profile(request, username):
    try:
        user_profile = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse("User not found", status=404)

    if request.user.is_authenticated:
        # Check if the logged-in user is viewing their own profile
        is_self = user_profile == request.user

        # Check if the logged-in user is following this user
        is_following = False
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