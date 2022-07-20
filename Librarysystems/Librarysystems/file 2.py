from django.urls import path
from Bookstore import views
from os import name

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:name'), views.greet_name, name='greet'

]