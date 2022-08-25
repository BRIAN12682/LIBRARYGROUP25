from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='lib-home'),
    path('afterlogin/', views.afterlogin_view, name = 'afterlogin'),
    path('index/', views.home_view, name='index'),
    path('borrowed/', views.borrowed_books_view, name='borrowed'),
    path('login/', auth_views.LoginView.as_view(template_name="library/login.html"), name='lib-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="library/logout.html"), name='lib-logout'),
    path('register/', views.register, name='lib-register'),
    path('home/', views.chat, name='lib-chat'),
    path('home_chat/', views.chat, name='chat-home'),

    path('send/', views.send_chat, name='chat-send'),
    path('renew/', views.get_messages, name='chat-renew'),
    path('library-home',views.lib_view,name='library-home'),
    path('add/<int:pk>', views.add_to_wishlist,name='add'),
    path('send/', views.send_chat, name='lib-send'),
    path('renew/', views.get_messages, name='lib-renew'),
    path('customer-home', views.home_view,name='customer-home'),
    path('my-profile', views.my_profile_view,name='my-profile'),
    path('wishlist', views.wishlist,name='wishlist'),
    path('remove-book/<int:pk>', views.remove_book,name='remove-book'),
    path('request/<int:id>/', views.requests, name='request'),
    path('request_book/<int:id>/', views.request_book,name='request_book'),
    path('search', views.search_view,name='/search'),
    path('fines', views.fines,name='fines'),
    path('return/<int:id>/', views.return_book, name='return'),
    path('return_book/<int:id>/', views.return_book_view,name='return_book'),
    path('', views.notification, name="home"),
    path('test/', views.test, name="home"),



]
