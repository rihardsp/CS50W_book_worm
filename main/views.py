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
from .models import User, SavedBook, Blog, Emails
from decouple import config

MAXPAGERESULTS = 10
API_GOOGLE = config('Google_Key')

### VIEWS OF THE APPLICATIONS

def index(request):
    
    """ Main index function loaded every time user opens website"""
    page = int(request.GET.get('page') or 1)
    all_blogs = Blog.objects.all().order_by('-timestamp')
     
    datapages = []

    counter= 0
    for each in all_blogs:
        book_key = each.book_id
        short_text = each.text[:200]
        long_text = each.text
        
        API_response = requests.get("https://www.googleapis.com/books/v1/volumes/"+book_key)
        API_results = API_response.json()
        volumeInfo = API_results['volumeInfo']

        datapages.append({
                    "card_id" : counter,
                    "author": each.user,
                    "title": each.title,
                    "book_title": volumeInfo["title"],
                    "book_authors": str(volumeInfo["authors"]),
                    "short_text": short_text,
                    "long_text": long_text,
                    "book_key": book_key,
                    "book_id": trycatch(trycatch(volumeInfo,"industryIdentifiers",firstobject=True,iterator=1),"identifier"),
                    "book_cover": trycatch(trycatch(volumeInfo,"imageLinks"),"smallThumbnail"),
                    "timestamp":each.timestamp
                    })
        counter += 1
    paginator = Paginator(datapages,MAXPAGERESULTS)
            
    blog_pages = paginator.page(page)

    
    
    return render(request, "index.html",{
        "page_name":"Forum",
        "forum":True,
        "blog_pages":blog_pages
    })
   



    
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
                    "author_name":str(trycatch(volumeInfo,"authors")).replace("["," ").replace("]","").replace("<b>",""),
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
            "comparer":True,
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

    raw_description = volumeInfo['description'].replace("</i>","").replace("—","").replace("<i>","").replace("<b>","").replace("</b>","").replace("<br>","").replace("<p>","").replace("</p>","")


    print(len(raw_description))
    text_description = {'short':str(raw_description[0:300])}
    try: 
        description_drop = raw_description.index("---") 
    except:
        description_drop = None
        
    # Retreive NY Times reviews
    
    #https://api.nytimes.com/svc/books/v3/reviews.json?author=Stephen+King&api-key=yourkey
    
    
    text_description['long'] = raw_description[300:description_drop]
    volumeInfo['text_description'] = text_description
    authors_list = volumeInfo['authors']
    counter = -1

    volumeInfo["URL_Amazon"] = "https://www.amazon.co.uk/s?k=" + volumeInfo['title'] + "=stripbooks&ref=nb_sb_noss_2"
    volumeInfo["URL_GoodReads"] = "https://www.goodreads.com/book/isbn/" + volumeInfo['industryIdentifiers'][0]['identifier']
    volumeInfo["URL_OpenLibrary"] = "https://openlibrary.org/isbn/" + volumeInfo['industryIdentifiers'][0]['identifier']
    volumeInfo["URL_LibraryThing"] = "https://www.librarything.com/isbn/" + volumeInfo['industryIdentifiers'][0]['identifier']
    print(volumeInfo['industryIdentifiers'][1]['identifier']) 
    general_info['authors_list'] = authors_list
    
    book_in_library = SavedBook.objects.filter(book_id=book_key).filter(user=request.user).count() > 0
    
    
    return render(request, "book_view.html",{
                "page_name":volumeInfo["title"],
                "comparer":True,
                "book_key":book_key,
                "general_info":general_info,
                "volumeInfo": volumeInfo,
                "book_in_library":book_in_library
            })
    
   
@login_required
def library_view(request):
    
    """ Library function that displays all books in the users library"""
    page = int(request.GET.get('page') or 1)
    users_books = SavedBook.objects.filter(user=request.user)
    no_library_results = users_books.count() == 0    
    library_pages = None
    if(no_library_results==False):
            
        datapages = []
        
        for each in users_books:
            
            API_response = requests.get("https://www.googleapis.com/books/v1/volumes/"+each.book_id)
            API_results = API_response.json()
            volumeInfo = API_results['volumeInfo']

            datapages.append({
                        "title": trycatch(volumeInfo,"title"),
                        "author_name":str(trycatch(volumeInfo,"authors")).replace("["," ").replace("]","").replace("<b>",""),
                        "book_key": each.book_id,
                        "book_id": trycatch(trycatch(volumeInfo,"industryIdentifiers",firstobject=True,iterator=1),"identifier"),
                        "publish_date": trycatch(volumeInfo,"publishedDate"),
                        "book_cover":trycatch(trycatch(volumeInfo,"imageLinks"),"smallThumbnail"),
                        "rating":trycatch(volumeInfo,"averageRating")
                        })
        paginator = Paginator(datapages,MAXPAGERESULTS)
                
        library_pages = paginator.page(page)

    
    return render(request, "library.html",{
        "page_name":"Library",
        "library":True,
        "no_books_exist":no_library_results,
        "library_pages": library_pages
    })
    
    
    
    
def trycatch(inobject,key,firstobject=False,iterator=None):
    try:
        if(firstobject):
            return inobject[key][iterator]
        else:
            return inobject[key]
    except:
        return False
        

    
def about_us_view(request):
    
    """ About us function to load about me section"""
    return render(request, "about_us.html",{"page_name":"About Me","about":True})
    
def contact_us_view(request):


    if(request.user.is_anonymous):
        user_name = request.user
        user_email = None
    else:    
        user = User.objects.get(username=request.user)
        user_name = user.username
        user_email = user.email
    
    """ Contact us function loads a website or processes a form """
    if request.method == 'POST':
        #try:
        if(request.user.is_anonymous):
            user = User.objects.get(username="AnonymousUser")
            user_name = request.POST["name"]
            user_email = request.POST["email"]

      
        save_email = Emails.objects.create(
            user=user,
            user_name = user_name,
            user_email = user_email,
            subject = request.POST["subject"],
            text = request.POST["message"])
        save_email.save()

        return HttpResponse("OK",status=201)
        #except Exception as e: 
        #    print(e)
        #    return HttpResponse(e,status=201)
    else:
        return render(request, "contact_us.html",{"user_name":user_name,"user_email":user_email, "page_name":"Contact Us","contact_us":True})

    
def settings_view(request):
    
    """ Users settings view"""
    return render(request, "settings.html",{"page_name":"Settings","active":"settings"})


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

@csrf_exempt
def book_toogle(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = request.user
            book_id=data.get("book_key")
            web_status = data.get("book_in_library")
    
            message = None
            db_status = str(SavedBook.objects.filter(book_id=book_id).filter(user=request.user).count() > 0)
    
            if(db_status == web_status):
                if(db_status == "False"):
                    print("Should go here")
                    book = SavedBook.objects.create(
                            user=request.user,
                            book_id=book_id,
                            )
                    book.save()
                    name = True
                    message = "Book added to the library"
                else:
                    SavedBook.objects.filter(book_id=book_id).filter(user=request.user).delete()
                    message = "Book removed from the library"
                    name = False
                return_status = 201
            else:
                message = "Web library status was not the same as DB library status"
                return_status = 403
        except Exception as e:
            print("...book_toggle exception:" + str(e))
            return_status=500
            message = "INTERNAL SERVER ERROR"
            name = None
            
    return JsonResponse({"message": message, "name":name}, status=return_status)
    
@csrf_exempt
def save_post(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = request.user
            book_id=data.get("book_key")
            blog_title = data.get("blog_title")
            blog_text = data.get("blog_text")
            
            if(blog_text != None and blog_title != None and book_id != None):
                blog = Blog.objects.create(
                    user=request.user,
                    book_id=book_id,
                    title = blog_title,
                    text = blog_text
                    )
                blog.save()
                return_status = 201
                message = "Blog " + blog_title + " saved successfully..."
            else:
                return_status = 400
                message = "All fields have to be filled out. Check that book_id, title and text are present"
            

        
        except Exception as e:
            
            print("...save_post exception:" + str(e))
            return_status=500
            message = str(e)
            
            
            
    return JsonResponse({"message": message}, status=return_status)