from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    watchlist = models.ManyToManyField("Listing", blank=True, related_name="watched_by")

    def __str__(self):
        return self.username
        

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places= 2)

    @property
    def highest_bid(self):
        highest_bid = self.bids.aggregate(models.Max("bid_amount"))["bid_amount__max"]
        return highest_bid or self.starting_bid 
    
    image_url = models.URLField(blank=True, null = True)
    category = models.CharField(max_length=64, blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_listings")
    closed = models.BooleanField(default=False)
    winner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="won_auctions")

    def __str__(self):
        return self.title

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.bidder.username} - {self.bid_amount}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.listing.highest_bid is None or self.bid_amount > self.listing.highest_bid:
            self.listing.highest_bid = self.bid_amount
            self.listing.save()

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f"{self.commenter.username}: {self.text[:20]}"
     