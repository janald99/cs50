import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Show, Rating, Review
from .forms import ReviewForm

def index(request, showpage=None):
    is_favorite_page = False
    if showpage == 'favorites':
        is_favorite_page = True
        shows = request.user.favorites.all().order_by('title')
    else:
        shows = Show.objects.all().order_by('title')
        
    return render(request, "capstone/index.html", {"shows": shows, "is_favorite_page": is_favorite_page})

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
    if request.method == "POST":
        # form submission
        creator = request.user
        title = request.POST.get("add-show-title")
        description = request.POST.get("add-show-description")
        genre = request.POST.get("add-show-genre")
        image_url = request.POST.get("add-show-image")
        new_show = Show(creator=creator,title=title,description=description,genre=genre, image_url=image_url)
        new_show.save()
        return HttpResponseRedirect(reverse("index"))  # Redirect to the show list after posting a new show.
    else:
        return render(request, "capstone/new_show.html")
    
def show_view(request, show_id):
    show =  Show.objects.get(pk=show_id)
    reviews = Review.objects.filter(show=show).order_by("-created_at")

    review_form = ReviewForm()
    if request.method == "POST":
        if "review_form_submit" in request.POST:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                text = review_form.cleaned_data["text"]
                review = Review(show=show, user=request.user, text=text)
                review.save()
                return HttpResponseRedirect(reverse("show_view", args=[show_id]))
        elif "favorites_submit" in request.POST:
            if request.user.is_authenticated:
                if show in request.user.favorites.all():
                    request.user.favorites.remove(show)
                    show.favorites.remove(request.user)
                else:
                    request.user.favorites.add(show)
                    show.favorites.add(request.user)
            return HttpResponseRedirect(reverse("show_view", args=[show_id]))
    
    is_in_favorites = show in request.user.favorites.all() if request.user.is_authenticated else False

    return render(request, "capstone/show_page.html", {
        "show": show,
        "reviews": reviews,
        "review_form": review_form,
        "is_in_favorites": is_in_favorites
    })

@login_required
def remove_from_favorites(request, show_id):
    show = Show.objects.get(pk=show_id)
    request.user.favorites.remove(show)
    return HttpResponseRedirect(reverse("favorites"))


@login_required
def rate_show(request, show_id):
    if request.method == 'POST':
        show =  Show.objects.get(pk=show_id)
        stars = request.POST.get('stars')
        if stars:
            stars = int(stars)
            # Ensure user hasn't rated the show before
            if not Rating.objects.filter(user=request.user, show=show).exists():
                # Create or update the rating
                rating, created = Rating.objects.get_or_create(user=request.user, show=show)
                rating.stars = stars
                rating.save()
                return HttpResponseRedirect(reverse('show_view', args=[show_id]))
            else:
                return HttpResponse("You have already rated this show.")
    return HttpResponse("Invalid request.")
