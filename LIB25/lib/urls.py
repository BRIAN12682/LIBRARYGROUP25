from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='lib-home'),
    path('afterlogin/', views.afterlogin_view, name = 'afterlogin'),
    path('index/', views.home_view, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name="library/login.html"), name='lib-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="library/logout.html"), name='lib-logout'),
    path('register/', views.register, name='lib-register'),
    path('home/', views.chat, name='lib-chat'),
    path('home_chat/', views.chat, name='chat-home'),
    path('dashboard/', views.dashboard, name='dashboard-page'),
    path('send/', views.send_chat, name='chat-send'),
    path('renew/', views.get_messages, name='chat-renew'),
    path('customer-home',views.lib_view,name='library'),
    path('add-to-cart/<int:pk>', views.add_to_cart_view,name='add-to-cart'),
    path('books/', views.books_view,name='books'),
    path('send/', views.send_chat, name='lib-send'),
    path('renew/', views.get_messages, name='lib-renew'),
    path('customer-home', views.home_view,name='customer-home'),
    path('my-profile', views.my_profile_view,name='my-profile'),
    path('edit-profile', views.edit_profile_view,name='edit-profile'),
    path('cart', views.cart_view,name='cart'),
    path('remove-from-cart/<int:pk>', views.remove_from_cart_view,name='remove-from-cart'),
    path('my-requested-books', views.my_request_view,name='my-requested-books'),
    path('request/<int:id>/', views.requests, name='request'),
    path('request_book/<int:id>/', views.request_book,name='request_book'),
    path('search', views.search_view,name='/search'),
    path('student_info', views.student_info,name='student_info'),
    path('book_view', views.view,name='book_view'),


    #path('request_book/', views.requests, name='request_book'),
    #path('send_request/', views.send_request, name='send_request'),
    #path('book_request/', views.get_book_request, name='book_request'),




]
