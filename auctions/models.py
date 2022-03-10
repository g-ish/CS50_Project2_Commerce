from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now, datetime
from datetime import timezone

''' 
three models needed
bids
auctions
comments

an auction can have many bids and comments
a bid can only have one auction
a comment can only have one auction
'''

class User(AbstractUser):
    watch_list = models.ManyToManyField('Auction', blank=True, related_name="watchers")

    def __str___(self):
        return self.username  


class Auction(models.Model):
    FURNITURE = "Furniture"
    ELECTRONICS = "Electronics"
    SPORTS_EQUIPMENT = "Sports Equipment"
    AUTOMOBILES = "Automobiles"
    OTHER = "Other"
    
    categories = [
    (FURNITURE, 'Furniture'),
    (ELECTRONICS, 'Electronics'),
    (SPORTS_EQUIPMENT, 'Sports Equipment'),
    (AUTOMOBILES, 'Automobiles'),
    (OTHER, 'Other'),
    ]
    
    owner = models.ForeignKey('User',  on_delete=models.CASCADE, related_name="listings")
    item_title = models.CharField(max_length=64)
    starting_bid = models.FloatField()
    item_description = models.CharField(max_length=900)
    item_category = models.CharField(choices=categories, max_length=64)
    creation_date = models.DateTimeField(auto_now_add=True)

    ended_date = models.DateTimeField(blank=True, null=True)
    auction_finished = models.BooleanField(blank=True, null=True)
    image_url = models.URLField(blank=True)
    class Meta:
        ordering = ['-creation_date']

    def __str___(self):
        return self.pk  

class Comment(models.Model): 
    owner = models.ForeignKey('User', on_delete=models.CASCADE, related_name="comments")
    auction = models.ForeignKey('AUction', on_delete=models.CASCADE)
    contents =  models.TextField(max_length=500)
    postedDate = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.owner.username} : {self.contents}"

class Bid(models.Model):
    owner = models.ForeignKey('User', on_delete=models.CASCADE, related_name="bids")
    auction = models.ForeignKey('Auction', on_delete=models.CASCADE, related_name="auctions")
    amount = models.DecimalField(max_digits=10,decimal_places=2)

# class AuctionPhotos(models.Model):
#     auction = models.ForeignKey(Auction, default=None, on_delete=models.CASCADE,related_name='images')

#     images = models.FileField(upload_to = 'images/')

#     def __str__(self):
#             return self.images.url
