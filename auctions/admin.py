from django.contrib import admin
from .models import Listing, Comment, Bid

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'starting_bid', 'creator')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('listing', 'commenter', 'text')

class BidAdmin(admin.ModelAdmin):
    list_display = ('bidder', 'listing', 'bid_amount')

admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid, BidAdmin)
