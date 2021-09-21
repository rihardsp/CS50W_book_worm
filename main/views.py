import json
import time
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from datetime import datetime
from django.utils.timezone import get_current_timezone
import pytz
from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import User


### VIEWS OF THE APPLICATIONS

def index(request):
    
    """ Main index function loaded every time user opens website"""
    return render(request, "index.html")
    
def library_view(request):
    
    """ Main index function loaded every time user opens website"""
    return render(request, "library.html")

def comparer_view(request):
    
    """ Main index function loaded every time user opens website"""
    return render(request, "comparer.html")
    
def about_us_view(request):
    
    """ Main index function loaded every time user opens website"""
    return render(request, "about_us.html")
    
def contact_us_view(request):
    
    """ Main index function loaded every time user opens website"""
    return render(request, "contact_us.html")
    
def profile_view(request):
    
    """ Main index function loaded every time user opens website"""
    return render(request, "profile.html")
    
    
def settings_view(request):
    
    """ Main index function loaded every time user opens website"""
    return render(request, "settings.html")


### API INTERACTIONS 


### LOGIN / LOGOUT / REGISTER SIDE OF THE APPLICATION
    
    
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
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")


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
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")

