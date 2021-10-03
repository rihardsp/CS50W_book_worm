from django.contrib.auth.models import AbstractUser
from django.db import models


# https://docs.djangoproject.com/en/3.2/ref/contrib/auth/

class User(AbstractUser):
    pass


class savedBook(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name = "user")
    book_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
class blog(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name = "user")
    book_id = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=2000)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
class emails(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name = "user")
    text = models.CharField(max_length=2000)
    timestamp = models.DateTimeField(auto_now_add=True)

    