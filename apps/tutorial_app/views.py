from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
def index(request):
    context = {'tutorials': ["Introduction to Python", "Introduction to Numpy"]}
    return render(request, "tutorial_app/tutorials.html", context) 