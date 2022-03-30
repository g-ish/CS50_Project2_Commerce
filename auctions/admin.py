from django.contrib import admin
from auctions.models import Auction, Comment, Bid, User, Watchlist

# Register your models here.

@admin.register(Auction)
@admin.register(Comment)
@admin.register(Bid)
@admin.register(User)
@admin.register(Watchlist)



class CommentAdmin(admin.ModelAdmin):
    pass

class BidAdmin(admin.ModelAdmin):
    pass

