from ast import Pass
from asyncio.windows_events import NULL
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Auction, Bid, Comment
from .forms import NewAuction, NewComment
from django.utils import timezone
from datetime import datetime as dt

# Unused
# def get_min_bid(current_price):
#     # based on ebay's minimum bid increments; https://www.ebay.co.uk/help/buying/bidding/automatic-bidding?id=4014&mkevt=1&mkcid=1&mkrid=710-53481-19255-0&campid=5336728181&customid=&toolid=10001
#     if current_price < 10:
#         return 0.05
#     elif current_price < 4.99:
#         return 0.20
#     elif current_price < 14.99:
#         return 0.5
#     elif current_price < 59.99:
#         return 1.00
#     elif current_price < 149.99:
#         return 2.00
#     elif current_price < 299.99:
#         return 5.00
#     elif current_price < 599.99:
#         return 10.00


def index(request):


    auctions = Auction.objects.filter(auction_finished=False).order_by('-creation_date').values()

    # attach the highest bid to each auction object
    for auction in auctions:
        highest_bid = Bid.objects.filter(auction=auction['id']).order_by('-amount').first()
        highest_bid = round(highest_bid.amount, 2)
        if highest_bid < auction['starting_bid']:
            auction['highest_bid'] = auction['starting_bid']
        else:
            auction['highest_bid'] = highest_bid
        auction['bid_count'] = Bid.objects.all().filter(auction=auction['id']).count()
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
        # if form.is_valid():
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
        
        return redirect(view_listing, new_auction.pk)
        
        # else:
        #     print('form invalid')

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
    bids = Bid.objects.all().filter(auction=auction)
    if not bids.exists():
        highest_bid = auction.starting_bid
    else:
        highest_bid = Bid.objects.filter(auction=auction).order_by('-amount').first()
        highest_bid = round(highest_bid.amount, 2)
    comments = Comment.objects.all().filter(auction=auction)

    # Creating the 'duration left' fields.
    time_left = auction.listing_duration - timezone.now()
    time_left = str(time_left).split(":")

    # 'days' only found in time_left if hours > 24. 
    if 'days' in time_left[0]:
        time = time_left[0].split(", ")
        days = time[0]
        hours = time[1]
    else:
        days = 0
        hours= time_left[0]
    minutes = time_left[1]



    bid_data = {
        'highest_bid' : highest_bid, 
        # new bid must be 10% above the previous
        'minimum_bid' : round(highest_bid * 0.1 + highest_bid,2),
        'bid_count' : Bid.objects.all().filter(auction=auction).count(),
        'days_remaining' : days,
        'hours_remaining': hours,
        'minutes_remaining': minutes
        }

    comments = Comment.objects.all().filter(auction=auction)
    listing = {
        'auction_pk' : auction.pk,
        'auction' : auction,
        'bid_data' : bid_data,
        'comments' : comments,
        }
    if request.method == "GET":
       return render(request, 'auctions/view_listing.html', {'listing' : listing})
    elif request.method == "POST":
        new_bid = Bid(owner = request.user, auction=auction, amount=request.POST["new-bid"])
        new_bid.save()
        return redirect(view_listing, pk)

def new_comment(request, pk):
    auction = Auction.objects.get(pk=pk)

    form = NewComment()
    if request.method == "GET":
        return render(request, 'auctions/new_comment.html', {'form' : form})
    else:
        new_comment = Comment(owner = request.user, auction=auction, contents=request.POST["new_comment"])
        new_comment.save()
        return redirect(view_listing, auction.pk)