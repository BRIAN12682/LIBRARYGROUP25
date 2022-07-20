from django.shortcuts import render
from django.http import HttpResponse

def greet_name(request,name):
    return HttpResponse(f'Hello, {name}')

def index(request):
    return HttpResponse('You are welcome.')