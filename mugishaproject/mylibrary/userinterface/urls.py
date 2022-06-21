from django.urls import path
from userinterface import views

urlpatterns=[
    path('', views.index, name='index'),
]