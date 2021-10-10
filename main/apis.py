import json

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .models import SavedBook, Blog


### API INTERACTIONS 

@csrf_exempt
@login_required
def book_toogle(request):
    
    """ Toggles between book being saved in the SavedBook(s) table and being deleted. Depends on the status of the book
    
    Parameters
        ----------
        request : request object, mandatory
            Request received from the client
    """
    
    
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
@login_required
def save_post(request):
    
    """ Saves users written blog in Blog(s) table. 
    
    Parameters
        ----------
        request : request object, mandatory
            Request received from the client
    """
    
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