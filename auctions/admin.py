from django.contrib import admin
from auctions.models import Auction, Comment, Bid, AuctionPhotos

# Register your models here.
@admin.register(Auction)
@admin.register(Comment)
@admin.register(Bid)
@admin.register(AuctionPhotos)




class CommentAdmin(admin.ModelAdmin):
    pass

class BidAdmin(admin.ModelAdmin):
    pass

class PictureInline(admin.StackedInline):
    model = AuctionPhotos

class AuctionAdmin(admin.ModelAdmin):
    inlines = [PictureInline]

