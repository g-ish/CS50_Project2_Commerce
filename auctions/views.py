from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auction
from .forms import NewAuction


def index(request):
    return render(request, "auctions/index.html")


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
        if form.is_valid():
            # Save the form into DB and use the PK to show the auction
                owner = request.user
                item_title = request.POST["item_title"]
                item_description = request.POST["item_description"]
                item_category = request.POST["item_category"]
                starting_bid = request.POST["starting_bid"]
                image_url = request.POST["image_url"]


                new_auction = Auction(owner=owner, item_title=item_title, starting_bid=starting_bid,
                    item_description=item_description, item_category=item_category, image_url=image_url)
                new_auction.save()


                # can't save photo until we have the object from Auction
                # image = request.POST["photo"]
                # image = AuctionPhotos(auction=new_auction, images=image)
                # image.save()


                return HttpResponseRedirect(reverse("view_listing", {"pk" : new_auction.pk} ))
        

    else:
        form = NewAuction()
        return render(request, 'auctions/create_listing.html', {'form' : form })

def view_user_listings(request):
     return render(request, 'auctions/my_listings.html')


def view_past_listings(request):
    pass

def view_listing(request):
    pass