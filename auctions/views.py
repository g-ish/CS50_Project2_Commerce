from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Auction, Bid, Comment
from .forms import NewAuction
from django.utils import timezone
from datetime import datetime as dt

def index(request):

    auctions = Auction.objects.all().order_by('-creation_date')


    return render(request, "auctions/index.html", {"auctions" : auctions})


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
    if request.method == "POST": 
        form = NewAuction(request.POST)

        print(request.POST['listing_duration'])
        if form.is_valid():
            # Save the form into DB and use the PK to show the auction
                owner = request.user
                item_title = request.POST["item_title"]
                item_description = request.POST["item_description"]
                item_category = request.POST["item_category"]
                starting_bid = request.POST["starting_bid"]
                image_url = request.POST["image_url"]
                listing_duration = request.POST['listing_duration']


                new_auction = Auction(owner=owner, item_title=item_title, starting_bid=starting_bid,
                    item_description=item_description, item_category=item_category, listing_duration=listing_duration, image_url=image_url)
                new_auction.save()


                # can't save photo until we have the object from Auction
                # image = request.POST["photo"]
                # image = AuctionPhotos(auction=new_auction, images=image)
                # image.save()

                
                return redirect(view_listing, new_auction.pk)
        
        else:
            print('form invalid')

    else:
        form = NewAuction()
        return render(request, 'auctions/create_listing.html', {'form' : form })

def view_user_listings(request):
     return render(request, 'auctions/my_listings.html')


def view_past_listings(request):
    pass

def view_listing(request, pk):
    auction = Auction.objects.get(pk=pk)
    
    comments = Comment.objects.all().filter(auction=auction).values()
    bids = Bid.objects.all().filter(auction=auction).values()

    # created new dedicated field for highest bid 
    # # get the highest bid while setting the minimum bid
    # highest_bid = bids.order_by('-amount')
    # highest_bid = float(highest_bid[0]['amount'])

    
    time_left = auction.listing_duration - timezone.now()
    time_left = str(time_left).split(":")
    
    days = time_left[0]
    hours = time_left[1]
    minutes = time_left[2].split(".")[0]


    bid_data = {
        'highest_bid' : auction.highest_bid,
        # new bid must be 10% above the previous
        'minimum_bid' : highest_bid * 0.1 + highest_bid,
        'bid_count' : bids.count(),
        'days_remaining' : days,
        'hours_remaining': hours,
        'minutes_remaining': minutes
        }

    


    comments = Comment.objects.all().filter(auction=auction)
    listing = {
        'auction' : auction,
        'bid_data' : bid_data,
        'comments' : comments,

    }

    return render(request, 'auctions/view_listing.html', {'listing' : listing})