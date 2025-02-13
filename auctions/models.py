from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta


def validate_listing_duration(date):
    if date - timedelta(hours=1) < timezone.now():
        raise ValidationError('Date cannot be in the past.',
                              params={'value': date},
                              )


class User(AbstractUser):
    # watch_list = models.ManyToManyField('Auction', blank=True, related_name="watchers")

    auctions_won = models.ForeignKey('Auction', on_delete=models.CASCADE, related_name="auctions_won", null=True)

    def __str___(self):
        return self.username



# Then use JS to dynamically show end date based on their input
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

    owner = models.ForeignKey('User', on_delete=models.CASCADE, related_name="listings")
    item_title = models.CharField(max_length=64)
    starting_bid = models.FloatField()
    item_description = models.CharField(max_length=900)
    item_category = models.CharField(choices=categories, max_length=64)
    creation_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(
        validators=[validate_listing_duration],
        help_text="Cannot be in the past."
    )

    ended_date = models.DateTimeField(blank=True, null=True)
    auction_finished = models.BooleanField(default=False)
    image_url = models.URLField(blank=True)

    class Meta:
        ordering = ['-creation_date']

    def __str___(self):
        return self.pk


class Comment(models.Model):
    owner = models.ForeignKey('User', on_delete=models.CASCADE, related_name="comments")
    auction = models.ForeignKey('Auction', on_delete=models.CASCADE)
    contents = models.TextField(max_length=500)
    posted_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['posted_date']

    def __str__(self):
        return f"{self.owner.username} : {self.contents}"

    def get_username(self):
        return self.owner.username


class Bid(models.Model):
    owner = models.ForeignKey('User', on_delete=models.CASCADE)
    auction = models.ForeignKey('Auction', on_delete=models.CASCADE)
    amount = models.FloatField()

    class Meta:
        ordering = ['amount']


class Watchlist(models.Model):
    owner = models.ForeignKey('User', on_delete=models.CASCADE)
    auction = models.ForeignKey('Auction', on_delete=models.CASCADE)
