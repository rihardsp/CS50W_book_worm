from django.shortcuts import render


def index(request):
    
    """ Main index function loaded every time user opens website"""
    return render(request, "index.html")
