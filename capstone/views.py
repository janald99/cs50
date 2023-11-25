import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Show

def index(request):
    return render(request, "capstone/index.html")

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
            return render(request, "capstone/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "capstone/login.html")


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
            return render(request, "capstone/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "capstone/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "capstone/register.html")

@login_required
def new_show(request):
    # if request.method == "POST":
    #     post_content = request.POST.get("post_content")
    #     # Create a new post and save it to the database
    #     new_post = Review(user=request.user, content=post_content)
    #     new_post.save()
    #     return HttpResponseRedirect(reverse("index"))  # Redirect to the same page after posting.
    # else:
    #     # Handle GET requests, if necessary
    #     return render(request, "capstone/index.html", {
    #         "posts": Thread.objects.all().order_by('-timestamp')
    #     })
    return HttpResponse("hey")
    
# @login_required
# def edit_post(request):
#     if request.method != "POST":
#         return JsonResponse({"error": "POST request required."}, status=400)

#     data = json.loads(request.body)
#     post_id = data.get("post_id")
#     edited_content = data.get("content")

#     post = Post.objects.get(id=post_id)

#     post.content = edited_content
#     post.save()

#     return JsonResponse({"success": True})

# @login_required
# def like_post(request):
#     if request.method != 'POST':
#         return JsonResponse({'error': 'POST request required.'}, status=400)

#     data = json.loads(request.body)
#     post_id = data.get('post_id')
#     action = data.get('action')

#     post = Post.objects.get(id=post_id)

#     if action == 'like':
#         post.likes.add(request.user)
#     elif action == 'unlike':
#         post.likes.remove(request.user)
#     else:
#         return JsonResponse({'error': 'Invalid action.'}, status=400)

#     post.save()

#     return JsonResponse({'success': True, 'like_count': post.likes.count()})

# def profile(request, username):
#     try:
#         user_profile = User.objects.get(username=username)
#     except User.DoesNotExist:
#         return HttpResponse("User not found", status=404)

#     is_self = False
#     is_following = False

#     if request.user.is_authenticated:
#         # Check if the logged-in user is viewing their own profile
#         is_self = user_profile == request.user

#         # Check if the logged-in user is following this user
#         if not is_self:
#             is_following = user_profile.followers.filter(id=request.user.id).exists()

#     # Retrieve the user's posts in reverse chronological order
#     user_posts = Post.objects.filter(user=user_profile).order_by('-timestamp')

#     return render(request, "network/profile.html", {
#         "user_profile": user_profile,
#         "is_self": is_self,
#         "is_following": is_following,
#         "user_posts": user_posts,
#     })


# @login_required
# def follow_user(request):
#     if request.method != "POST":
#         return JsonResponse({"error": "POST request required."}, status=400)

#     data = json.loads(request.body)
#     username = data.get("username")

#     user_to_follow = User.objects.get(username=username)

#     action = data.get("action")

#     if action == "follow":
#         user_to_follow.followers.add(request.user)
#         request.user.following.add(user_to_follow) 
#         request.user.save()
#         user_to_follow.save()
#         print(user_to_follow.followers)
#         print(request.user.following)
#         response_data = {
#             "message": "User followed successfully.",
#             "followersCount": user_to_follow.followers.count(),
#             "followingCount": user_to_follow.following.count(),
#         }
#     elif action == "unfollow":
#         user_to_follow.followers.remove(request.user)
#         request.user.following.remove(user_to_follow)
#         request.user.save()
#         user_to_follow.save()
#         print(request.user.following)
#         response_data = {
#             "message": "User unfollowed successfully.",
#             "followersCount": user_to_follow.followers.count(),
#             "followingCount": user_to_follow.following.count(),
#         }
#     else:
#         response_data = {"message": "Invalid action."}

#     return JsonResponse(response_data)