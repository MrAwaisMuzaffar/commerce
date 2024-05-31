from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Listing, Bid, Comment,User


def index(request):
    current_price = []
    for obj in Listing.objects.all():
        if Bid(obj.id).amount > obj.starting_bid:
             current_price.append(Bid(obj.id).amount)
        else:
            current_price
    return render(request, "auctions/index.html",{
                  "listings": Listing.objects.all(),
                   "current_price": current_price 
                  }
                  )


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


def new_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image_url = request.POST["image_url"]
        category = request.POST["category"]
        created_by = request.user

        # Attempt to create new listing
        try:
            listing = Listing.objects.create(
                title=title,
                description=description,
                starting_bid=starting_bid,
                image_url=image_url,
                category=category,
                created_by=created_by
            )
            listing.save()
        except IntegrityError:                                  
            return render(request, "auctions/new_listing.html", {   
                "message": "Error creating new listing."
            })
        return HttpResponseRedirect(reverse("index"))
    else:
       return render (request, "auctions/new_listing.html")
    
def display_item(request,key):
    entry = Listing.objects.get(id=key)
    comments = entry.comment_set.all()
    bids = entry.bid_set.all()
    return render(request, "auctions/item.html", {
        "item": entry,
        "bids": bids,
        "comments": comments
    }) 