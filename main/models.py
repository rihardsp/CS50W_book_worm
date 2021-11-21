from django.contrib.auth.models import AbstractUser
from django.db import models


# https://docs.djangoproject.com/en/3.2/ref/contrib/auth/

class User(AbstractUser):
    pass


class SavedBook(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name = "library_user")
    book_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
class Blog(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name = "blog_user")
    book_id = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=2000)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
class Emails(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name = "emails_user")
    user_name = models.CharField(max_length=200, default=None)
    user_email = models.CharField(max_length=200, default=None)
    subject = models.CharField(max_length=200)    
    text = models.CharField(max_length=2000)
    timestamp = models.DateTimeField(auto_now_add=True)

    
