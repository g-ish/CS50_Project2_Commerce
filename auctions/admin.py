from django.contrib import admin
from auctions.models import Auction, Comment, Bid

# Register your models here.
@admin.register(Auction)
@admin.register(Comment)
@admin.register(Bid)





class CommentAdmin(admin.ModelAdmin):
    pass

class BidAdmin(admin.ModelAdmin):
    pass

