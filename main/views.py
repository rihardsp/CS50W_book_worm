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

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import User
from decouple import config

MAXPAGERESULTS = 10
API_GOOGLE = config('Google_Key')

### VIEWS OF THE APPLICATIONS

def index(request):
    
    """ Main index function loaded every time user opens website"""
    return render(request, "index.html",{"page_name":"Forum"})
   
   
@login_required
def library_view(request):
    
    """ Main index function loaded every time user opens website"""
    return render(request, "library.html",{"page_name":"Library"})

def search_book(requests,searchpattern):
    print("searchBook pressed" + searchpattern)
    
@csrf_exempt
@login_required
def comparer_view(request):
    """ Comparer view loads searchbar or search_results"""
    search_pages = []
    search_results = False
    search_failed = False
    print("Comparer View Loading")
    
    searchtext = request.GET.get('search-text','')
    print("searchtext: " + searchtext)
    
    if(searchtext != ""):
        page = int(request.GET.get('page') or 1)
        print("SEARCH FORM RECEIVED")
        print("PAGE RECEVEID: " + str(page))
        print("USER SEARCHED FOR: " + searchtext)
        try: 
            startIndex = (page * 10) - 10
            search_response = requests.get("https://www.googleapis.com/books/v1/volumes?q="+searchtext+"&startIndex="+ str(startIndex) + "&maxResults="+str(MAXPAGERESULTS))
            print("Comparer_view API request returned: " + str(search_response))
            search_results = search_response.json()
            print("Comparer_view API items found: "+ str(search_results['totalItems']))
            if(search_results['totalItems'] == 0):
                raise Exception("Total Items Returned are 0")
        except Exception as e:
            print("Comparer_view API request failed: " + str(e))
            search_failed = True
            
        
        if(search_failed == False):

            return_docs = search_results['items']
            
            print("Comparer_view API items returned: "+ str(len(return_docs)))
            
            print(len(return_docs))
            datapages = []
            
            counter = 0

            for each in return_docs:
                
                volumeInfo = trycatch(each,"volumeInfo")
                datapages.append({
                    "title": trycatch(volumeInfo,"title"),
                    "author_name":str(trycatch(volumeInfo,"authors")).replace("["," ").replace("]",""),
                    "book_key": trycatch(each,"id"),
                    "book_id": trycatch(trycatch(volumeInfo,"industryIdentifiers",firstobject=True,iterator=1),"identifier"),
                    "publish_date": trycatch(volumeInfo,"publishedDate"),
                    "book_cover":trycatch(trycatch(volumeInfo,"imageLinks"),"smallThumbnail"),
                    "rating":trycatch(volumeInfo,"averageRating")
                    })
                counter += 1
                
            datapages.sort(key=lambda x: x["rating"], reverse=True)
            x = 0
            for each in range(startIndex):
                datapages.insert(0,x)
                x -= 1
                
                
            counter = search_results['totalItems'] - counter  - startIndex    
            
            for each in range(counter):
                datapages.append({})
                
            
            print(len(datapages))
            
        
            paginator = Paginator(datapages,MAXPAGERESULTS)
            
            search_pages = paginator.page(page)
            
            print("Pages: " + str(search_pages)) 
            search_results = True
    
    
    return render(request, "comparer.html",{
            "page_name":"Comparer",
            "search_results":search_results,
            "search_failed":search_failed,
            "search_pages": search_pages,
            "searchtext":searchtext
        })
    

def book_view(request,book_key,book_id):
    print("Book Loaded: "+ book_key + " / " + book_id)
    
    # Google Books APIs Main API Driving Stuff https://developers.google.com/books/docs/dynamic-links?csw=1
    try:
        API_except_status = False
        # API Example https://www.googleapis.com/books/v1/volumes/GNnxzQEACAAJ
        # API Documentation - https://developers.google.com/books/docs/v1/using
        API_response = requests.get("https://www.googleapis.com/books/v1/volumes/"+book_key)
        API_results = API_response.json()
        general_info = API_results
    except Exception as e:
        print("Book_view API request failed: " + str(e))
        API_except_status = True
    

    volumeInfo = general_info['volumeInfo']  

    raw_description = volumeInfo['description'].replace("</i>","").replace("—","").replace("<i>","")


    print(len(raw_description))
    text_description = {'short':str(raw_description[0:300])}
    try: 
        description_drop = raw_description.index("---") 
    except:
        description_drop = None
        
  
    text_description['long'] = raw_description[300:description_drop]
    volumeInfo['text_description'] = text_description
    authors_list = volumeInfo['authors']
    counter = -1
    
    ## OpenLibrary API - rating about the book
    
    general_info['authors_list'] = authors_list
    return render(request, "book_view.html",{
                "page_name":volumeInfo["title"],
                "book_key":book_key,
                "general_info":general_info,
                "volumeInfo": volumeInfo
            })
    
    
def trycatch(inobject,key,firstobject=False,iterator=None):
    try:
        if(firstobject):
            return inobject[key][iterator]
        else:
            return inobject[key]
    except:
        return False
        
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
    elif "key" in inobject:
        return inobject["key"].replace("works","olid")
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



