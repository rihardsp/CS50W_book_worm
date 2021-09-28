import json
import time
# TO BE DONE import logging
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
import requests
from django import forms

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import User

MAXPAGERESULTS = 10

### VIEWS OF THE APPLICATIONS



def index(request):
    
    """ Main index function loaded every time user opens website"""
    return render(request, "index.html",{"page_name":"Forum"})
   
   
@login_required
def library_view(request):
    
    """ Main index function loaded every time user opens website"""
    return render(request, "library.html",{"page_name":"Library"})
    
@csrf_exempt
@login_required
def comparer_view(request):
    """ Comparer view loads searchbar or search_results"""

    if request.method == "POST":
        
        print("SEARCH FORM RECEIVED")
        searchtext = request.POST["search-text"]
        print("USER SEARCHED FOR: " + searchtext)
        try:
            API_except_status = False
            search_response = requests.get("https://openlibrary.org/search.json?&q="+searchtext)
            search_results = search_response.json()
        except Exception as e:
            print("Comparer_view API request failed: " + str(e))
            API_except_status = True
        
        if(API_except_status == False):
            print("Comparer_view API results returned: "+ str(search_results['numFound']))
         
            return_docs = search_results['docs']

            datapages = []
            
            for each in return_docs:

                
                
                datapages.append({
                    "title":each["title"],
                    "author_name":trycatch(each,"author_name"),
                    "book_key":each['key'].replace("/works/",""),
                    "publish_date": trycatch(each,"publish_date"),
                    "book_cover":book_cover(each)
                    })

   
            paginator = Paginator(datapages,MAXPAGERESULTS)
            
            search_pages = paginator.page(1)
            
            print("Pages: " + str(search_pages)) 
            
            return render(request, "comparer.html",{
                    "page_name":"Comparer",
                    "search_results":True,
                    "search_failed":False,
                    "search_pages": search_pages
                })
    
        else:
            return render(request, "comparer.html",{
                    "page_name":"Comparer",
                    "search_results":False,
                    "search_failed":True
                })
            

           

    
    
    
    return render(request, "comparer.html",{
        "page_name":"Comparer",
        "search_results":False,
        "search_failed":False
    })
    
def book_view(request,book_key):
    print("Book Loaded: "+ book_key)
    
    ## OpenLibrary API - general information about the book
    try:
        API_except_status = False
        API_response = requests.get("https://openlibrary.org/books/"+book_key+".json")
        API_results = API_response.json()
        general_info = API_results
    except Exception as e:
        print("Book_view API request failed: " + str(e))
        API_except_status = True
        
    raw_description = general_info['description']['value']

    general_info['description']['short'] = raw_description[0:300]
    general_info['description']['long'] = raw_description[300:raw_description.index("----------")]
    # Google Books APIs https://developers.google.com/books/docs/dynamic-links?csw=1
    # Amazon API
    authors = general_info['authors']
    authors_list = []
    for each in authors: 
        Author_API_response = requests.get("https://openlibrary.org/"+each['author']['key']+".json")
        
        authors_list.append({
            'name' : str(Author_API_response.json()['name']),
            'wikilink':str(Author_API_response.json()['wikipedia']),
            'description':str(Author_API_response.json()['bio']['value'])
            }) 
    
    general_info['authors_list'] = authors_list
    return render(request, "book_view.html",{
                "page_name":API_results["title"],
                "book_key":book_key,
                "general_info":general_info
            })
    
    
def trycatch(inobject,key):
    try:
        return inobject[key][0]
    except:
        return None
        
def book_cover(inobject):
    if "isbn" in inobject:
        return "isbn/"+inobject["isbn"][0]
    elif "olid" in inobject:
        return "olid/"+inobject["olid"][0]
    elif "id" in inobject:
        return "id/"+inobject["id"][0] 
    elif "lccn" in inobject:
        return "lccn/"+inobject["lccn"][0]  
    elif "oclc" in inobject:
        return "oclc/"+inobject["oclc"][0] 
    elif "goodreads" in inobject:
        return "goodreads/"+inobject["goodreads"][0] 
    else:
        return None
   

    
def about_us_view(request):
    
    """ Main index function loaded every time user opens website"""
    return render(request, "about_us.html",{"page_name":"About Us"})
    
def contact_us_view(request):
    
    """ Main index function loaded every time user opens website"""
    return render(request, "contact_us.html",{"page_name":"Contact Us"})
    
def profile_view(request):
    
    """ Main index function loaded every time user opens website"""
    return render(request, "profile.html",{"page_name":"Your Profile"})
    
    
def settings_view(request):
    
    """ Main index function loaded every time user opens website"""
    return render(request, "settings.html",{"page_name":"Settings"})


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
