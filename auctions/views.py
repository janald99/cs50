from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Max 
from django.db import IntegrityError

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


from .models import User, Listing, Bid, Comment
from .forms import CreateListingForm, BidForm, CommentForm


def index(request):
    active_listings = Listing.objects.filter(closed=False)
    return render(request, "auctions/index.html", {
        "listings": active_listings
    })

def closed_listings_view(request):
    closed_listings = Listing.objects.filter(closed=True)
    return render(request, "auctions/closed_listings.html", {
        "listings": closed_listings
    })

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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.creator = request.user
            listing.save()
            return HttpResponseRedirect(reverse("index"))
    else:
            form = CreateListingForm()

    return render(request, "auctions/create_listing.html", {
        "form": form
    })

def listing_view(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    comments = Comment.objects.filter(listing=listing).order_by("-id")
    
    bid_form = BidForm()
    comment_form = CommentForm()

    won_auction = False
    if listing.winner == request.user:
        won_auction = True
    
    if request.method == "POST":
        if "bid_form_submit" in request.POST:
            if not listing.closed:
                bid_form = BidForm(request.POST)
                if bid_form.is_valid():
                    bid_amount = bid_form.cleaned_data["bid_amount"]
                    highest_bid = listing.highest_bid
                    if bid_amount >= listing.starting_bid and (highest_bid is None or bid_amount > highest_bid):
                        bid = Bid(listing=listing, bidder = request.user, bid_amount = bid_amount)
                        bid.save()
                        highest_bid = bid_amount
                        return HttpResponseRedirect(reverse("listing", args=[listing_id]))
                    else:
                        bid_form.add_error("bid_amount", "Bid must be larger than current bid.")
                else:
                    print("Bid form errors:", bid_form.errors)
            else:
                bid_form = BidForm()
                bid_form.errors['__all__'] = bid_form.error_class(["Auction is closed. No new bids can be added."])
                
        elif "comment_form_submit" in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                text = comment_form.cleaned_data["text"]
                comment = Comment(listing=listing, commenter = request.user, text = text)
                comment.save()
                return HttpResponseRedirect(reverse("listing", args=[listing_id]))
            
        elif "watchlist_submit" in request.POST:
            if request.user.is_authenticated:
                if listing in request.user.watchlist.all():
                    request.user.watchlist.remove(listing)
                else:
                    request.user.watchlist.add(listing)
            return HttpResponseRedirect(reverse("listing", args=[listing_id]))

        elif "close_auction" in request.POST:
            if listing.creator == request.user and not listing.closed:  
                # Check if there's a highest bidder
                highest_bid = listing.bids.aggregate(Max("bid_amount"))["bid_amount__max"]
                if highest_bid is not None:
                    winner_bid = listing.bids.filter(bid_amount=highest_bid).first()
                    if winner_bid:
                        listing.winner = winner_bid.bidder
                    else:
                        listing.winner = None
                    listing.save()
                    
                    if winner_bid.bidder == request.user:
                        won_auction = True

                # Close the auction and mark listing as closed
                listing.closed = True
                listing.save()

    is_in_watchlist = listing in request.user.watchlist.all() if request.user.is_authenticated else False


    return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": comments,
        "bid_form": bid_form,
        "comment_form": comment_form,
        "is_in_watchlist": is_in_watchlist,
        "won_auction": won_auction if request.user.is_authenticated else False
    })

@login_required
def watchlist(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    watchlist = request.user.watchlist.all()

    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })

@login_required
def remove_from_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    request.user.watchlist.remove(listing)
    return HttpResponseRedirect(reverse("watchlist"))


def categories(request):
    categories = set(listing.category for listing in Listing.objects.filter(category__isnull=False))

    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category_listings(request, category):
    listings = Listing.objects.filter(category=category)

    return render(request, "auctions/category_listings.html", {
        "category": category,
        "listings": listings
    })
