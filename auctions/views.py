from ast import Pass
from asyncio.windows_events import NULL
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Auction, Bid, Comment, Watchlist
from .forms import NewAuction, NewComment
from django.utils import timezone
from datetime import datetime as dt

def index(request):
    print(Auction.categories)

    auctions = Auction.objects.filter(auction_finished=False).order_by('-creation_date').values()
    # attach the highest bid to each auction object
    for auction in auctions:
        highest_bid = Bid.objects.filter(auction=auction['id']).order_by('-amount').first()
        try:
            highest_bid = round(highest_bid.amount, 2)
            auction['highest_bid'] = highest_bid
        except:
            auction['highest_bid'] = auction['starting_bid']
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
    time = str(timezone.now())
    if request.method == "POST": 
        form = NewAuction(request.POST)

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
    user = request.user
    auctions = Auction.objects.filter(auction_finished=False, owner=user).order_by('-creation_date').values()

    # attach the highest bid to each auction object
    for auction in auctions:
        highest_bid = Bid.objects.filter(auction=auction['id']).order_by('-amount').first()
        try:
            highest_bid = round(highest_bid.amount, 2)
            auction['highest_bid'] = highest_bid
        except:
            auction['highest_bid'] = auction['starting_bid']
        auction['bid_count'] = Bid.objects.all().filter(auction=auction['id']).count()
    return render(request, "auctions/my_listings.html", {"auctions" : auctions})





def view_past_listings(request):
    auctions = Auction.objects.filter(auction_finished=True).order_by('-creation_date').values()

    # attach the highest bid to each auction object
    for auction in auctions:
        highest_bid = Bid.objects.filter(auction=auction['id']).order_by('-amount').first()
        try:
            highest_bid = round(highest_bid.amount, 2)
            auction['highest_bid'] = highest_bid
        except:
            auction['highest_bid'] = auction['starting_bid']
        auction['bid_count'] = Bid.objects.all().filter(auction=auction['id']).count()
    return render(request, "auctions/past_listings.html", {"auctions" : auctions})

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
        watchers = Watchlist.objects.filter(owner=request.user, auction=auction.id)
        on_watch = False
        for watcher in watchers: 
            if watcher.owner.get_username() == request.user.get_username():
                on_watch = True
            else:
                on_watch = False
        return render(request, 'auctions/view_listing.html', {'listing' : listing, 'on_watch': on_watch})
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

def my_watchlist(request):

    watchers = Watchlist.objects.filter(owner=request.user)
    all_auctions = Auction.objects.all()

    # Get the highest bid and bid counts for each auction.
    def get_bid_data(auction_id):
        try:
            bid_data = Bid.objects.filter(auction=auction_id).order_by('-amount').first()
            highest_bid = bid_data.amount
        except: 
            bid_data = Auction.objects.get(id=e.auction.id)
            highest_bid = bid_data.starting_bid
        return {'highest_bid': round(highest_bid, 2), 'bid_count' : Bid.objects.all().filter(auction=auction_id).count()}

    # For each auction in the users watchlist, get the basic details 
    # to populate the watchlist. 
    auctions = []
    for e in watchers:
        bid_data = get_bid_data(e.auction.id)
        auction = Auction.objects.get(id=e.auction.id)
        auctions.append({
            'id': auction.id,
            'image_url': auction.image_url,
            'item_title': auction.item_title,
            'highest_bid': bid_data['highest_bid'],
            'bid_count': bid_data['bid_count']})
            
    return render(request, 'auctions/my_watchlist.html', {'auctions': auctions})
 
def add_watchlist(request, pk):

    auction = Auction.objects.get(pk=pk)
    watcher = Watchlist.objects.filter(owner=request.user, auction=auction.id)
    if not watcher.exists():
        aWatchlist = Watchlist(owner = request.user, auction=auction)
        aWatchlist.save()
    return redirect(view_listing, pk)

def delete_watchlist(request, pk):
    # remove from watchlist 
    auction = Auction.objects.get(pk=pk)
    watcher = Watchlist.objects.filter(owner=request.user, auction=auction.id)
    if watcher.exists():
        watcher.delete()

    return redirect(view_listing, pk)