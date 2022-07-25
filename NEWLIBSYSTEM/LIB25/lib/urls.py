
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='lib-home'),
    path('afterlogin/', views.afterlogin_view),
    path('index/', views.home_view, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name="library/login.html"), name='lib-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="library/logout.html"), name='lib-logout'),
    path('register/', views.register, name='lib-register'),
    path('home/', views.home, name='lib-home'),
    path('dashboard/', views.dashboard, name='dashboard-page'),








    path('profile/', views.profile, name='lib-profile'),
    path('manage-profile/', views.update_profile, name='manage-profile'),
    path('send/', views.send_chat, name='lib-send'),
    path('renew/', views.get_messages, name='lib-renew'),




    path('search', views.search_view,name='search'),
    path('request/', views.request_home_view,name='request_view'),
    path('request_detail/', views.my_request_view,name='request_view_det'),
    path('update-order/<int:pk>', views.update_request_view,name='update-order'),
    path('customer-home', views.home_view,name='customer-home'),
]
