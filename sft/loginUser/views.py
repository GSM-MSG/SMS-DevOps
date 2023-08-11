from django.shortcuts import render
import os

def index(request):
    print("test")
    return render(request, 'info.html')