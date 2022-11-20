from ast import Pass
from asyncio.windows_events import NULL
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Auction, Bid, Comment, Watchlist
from .forms import NewAuction, NewComment
from django.utils import timezone
from datetime import datetime as dt


def index(request):
    auctions = Auction.objects.filter(auction_finished=False).order_by('-creation_date').values()
    # attach the highest bid and bid counts to each auction object
    for auction in auctions:
        highest_bid = Bid.objects.filter(auction=auction['id']).order_by('-amount').first()
        try:
            highest_bid = round(highest_bid.amount, 2)
            auction['highest_bid'] = highest_bid
        except:
            auction['highest_bid'] = auction['starting_bid']
        auction['bid_count'] = Bid.objects.all().filter(auction=auction['id']).count()
    return render(request, "auctions/index.html", {"auctions": auctions})


def category_filter(request):
    categories = Auction.categories

    if request.method == "GET":
        return render(request, "auctions/category_view.html", {'categories': categories})
    else:
        category = request.POST["category"]
        auctions = Auction.objects.filter(item_category=category).order_by('-creation_date').values()
        # attach the highest bid to each auction object
    for auction in auctions:
        highest_bid = Bid.objects.filter(auction=auction['id']).order_by('-amount').first()
        try:
            highest_bid = round(highest_bid.amount, 2)
            auction['highest_bid'] = highest_bid
        except:
            auction['highest_bid'] = auction['starting_bid']
        auction['bid_count'] = Bid.objects.all().filter(auction=auction['id']).count()
    return render(request, "auctions/category_view.html", {
        "auctions": auctions,
        'categories': categories,
        'category': category})


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


@login_required
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
        # try:
        user = User.objects.create_user(username, email, password)
        user.save()

        # except IntegrityError:
        #     print(IntegrityError)
        #     return render(request, "auctions/register.html", {
        #         "message": "Username already taken."
        #     })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):
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
        expiry_date = request.POST['expiry_date']

        new_auction = Auction(owner=owner, item_title=item_title, starting_bid=starting_bid,
                              item_description=item_description, item_category=item_category, expiry_date=expiry_date,
                              image_url=image_url)
        new_auction.save()
        return redirect(view_listing, new_auction.pk)
        # else:
        #     print('form invalid')
    else:
        form = NewAuction()
        return render(request, 'auctions/create_listing.html', {'form': form})


# view the listings owned by logged in user
@login_required
def view_user_listings(request):
    user = request.user
    auctions = Auction.objects.filter(owner=user).order_by('-creation_date').values()

    # attach the highest bid to each auction object
    for auction in auctions:
        highest_bid = Bid.objects.filter(auction=auction['id']).order_by('-amount').first()
        try:
            highest_bid = round(highest_bid.amount, 2)
            auction['highest_bid'] = highest_bid
        except:
            auction['highest_bid'] = auction['starting_bid']
        auction['bid_count'] = Bid.objects.all().filter(auction=auction['id']).count()
    return render(request, "auctions/my_listings.html", {"auctions": auctions})


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
    return render(request, "auctions/past_listings.html", {"auctions": auctions})


def view_listing(request, pk):
    auction = get_auction(pk, request.user)

    if request.method == "GET":
        return render(request, 'auctions/view_listing.html',
                      {'listing' : auction})
    elif request.method == "POST":
        auction = Auction.objects.get(pk=pk)
        new_bid = Bid(owner=request.user, auction=auction, amount=request.POST["new-bid"])
        new_bid.save()
        return redirect(view_listing, pk)


@login_required
def new_comment(request, pk):
    auction = Auction.objects.get(pk=pk)

    form = NewComment()
    if request.method == "GET":
        return render(request, 'auctions/new_comment.html', {'form': form})
    else:
        new_comment = Comment(owner=request.user, auction=auction, contents=request.POST["new_comment"])
        new_comment.save()
        return redirect(view_listing, auction.pk)


@login_required
def my_watchlist(request):
    watchers = Watchlist.objects.filter(owner=request.user)
    # all_auctions = Auction.objects.all()

    # Get the highest bid and bid counts for each auction.
    def get_bid_data(auction_id):
        try:
            bid_data = Bid.objects.filter(auction=auction_id).order_by('-amount').first()
            highest_bid = bid_data.amount
        except:
            bid_data = Auction.objects.get(id=e.auction.id)
            highest_bid = bid_data.starting_bid
        return {'highest_bid': round(highest_bid, 2), 'bid_count': Bid.objects.all().filter(auction=auction_id).count()}

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


@login_required
def add_watchlist(request, pk):
    auction = Auction.objects.get(pk=pk)
    watcher = Watchlist.objects.filter(owner=request.user, auction=auction.id)
    if not watcher.exists():
        aWatchlist = Watchlist(owner=request.user, auction=auction)
        aWatchlist.save()
    return redirect(view_listing, pk)


@login_required
def delete_watchlist(request, pk):
    # remove from watchlist 
    auction = Auction.objects.get(pk=pk)
    watcher = Watchlist.objects.filter(owner=request.user, auction=auction.id)
    if watcher.exists():
        watcher.delete()

    return redirect(view_listing, pk)


@login_required
def close_listing(request, action, pk):
    if action == "delete":
        auction = Auction.objects.get(pk=pk)
        auction.delete()
        return redirect(index)
    elif action == "accept":
        auction = Auction.objects.get(pk=pk)
        auction.auction_finished = True
        auction.save()
        return redirect(view_listing, pk)
    else:
        return redirect(view_listing, pk)

    # Todo: Stop user from creating a listing in the past? Do from within the create listing page?


def get_auction(pk, user):
    auction = Auction.objects.get(pk=pk)
    comments = Comment.objects.all().filter(auction=auction)
    bids = Bid.objects.all().filter(auction=auction)

    # Get the highest bid, if no highest bid then assign starting bid
    if not bids.exists():
        highest_bid = auction.starting_bid
        highest_bid_amount = highest_bid
    else:
        highest_bid = Bid.objects.filter(auction=auction).order_by('-amount').first()
        highest_bid_amount = round(highest_bid.amount, 2)



    # If auction is not finished but time expired then set as finished.
    if auction.expiry_date < timezone.now() and not auction.auction_finished:
        auction.auction_finished = True
        auction.save()

    if auction.auction_finished:
        time_remaining = "Ended."
        if not bids:
            status = "ended"
        if bids and highest_bid.owner == user:
            status = "won" #let bid owner know there's a winner
        elif bids and auction.owner == user:
            status = "finished" #let auction owner know there's a winner
        else:
            status = "ended"

    else:
        status = 'active'
        time_left = auction.expiry_date - timezone.now()
        # converting the difference to a 'x days, y hours, z minutes format.
        time_left = str(time_left).split(":")
        if 'days' in time_left[0]:
            time = time_left[0].split(", ")
            days = time[0] + ", "
            hours = time[1]
        else:
            days = ""
            hours = time_left[0]
        minutes = time_left[1]
        time_remaining = str(days) + " " + str(hours) + " hours, " + str(minutes) + " minutes remaining."

    watchers = Watchlist.objects.filter(auction=auction.id)
    on_watch = False
    for watcher in watchers:
        if watcher.owner.get_username() == user.get_username():
            on_watch = True
        else:
            on_watch = False
    watch_count = Watchlist.objects.filter(auction=auction.id).count()

    # Flag to show special commands (delete, accept bid) to user if owner
    if auction.owner == user:
        owner = True
    else:
        owner = False

    bid_data = {
        'highest_bid': highest_bid,
        # new bid must be 10% higher than previous bid
        'minimum_bid': round(highest_bid_amount * 0.1 + highest_bid_amount,2),
        'bid_count': Bid.objects.all().filter(auction=auction).count(),
        'time_remaining': time_remaining,
    }

    listing = {
        'auction': auction,
        'auction_pk': auction.pk,
        'bid_data': bid_data,
        'comments': comments,
        'owner': owner,
        'on_watch': on_watch,
        'watch_count': watch_count,
        'status': status,
    }
    return listing
