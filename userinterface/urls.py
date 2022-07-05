from django.contrib import admin
from django.urls import include, path
from . import views
urlpatterns = [
    path('userinterface/',include('userinterface.urls')),
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('index/',views.index,name='index'),
    path('home/',views.home,name='home'), 
]
