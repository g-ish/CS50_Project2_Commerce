from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

class User(AbstractUser):
    watch_list = models.ManyToManyField(Auction)




''' 
three models needed
bids
auctions
comments

an auction can have many bids and comments
a bid can only have one auction
a comment can only have one auction
'''


class Auction(models.Model):
    categories = [
    ('Furniture'),
    ('Electronics'),
    ('Sports Equipment'),
    ('Automobiles'),
    ('Other'),
    ]

    item_description = models.CharField(max_length=30)
    item_category = models.CharField(choices=categories)

    creation_date = DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=user_directory_path)

    owner = models.ForeignKey(User, on_delete=Models.CASCADE)
    bidders = models.ManyToManyField(User)

    ended_date = DateTimeField(default=timezone.now)
    auction_finished = models.BooleanField()



def user_directory_path(instance, filename):
    return 'user_{0},{1}'.format(instance.user.id,filename)

class Comment(models.Model): 
    owner = models.ForeignKey(User, on_delete)
    contents =  models.TextField(max_length=500)
    