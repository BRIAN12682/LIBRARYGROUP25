from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import chatMessages, Books, Request, IssueBook
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User as UserModel
from django.db.models import Q
import json, datetime
from django.contrib.auth.models import User
from . import models, forms
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.core import serializers
from django.shortcuts import render, HttpResponse
from channels.layers import get_channel_layer


def home_view(request):
    if request.user.is_authenticated:
        books = models.Books.objects.all()
        if 'book_ids' in request.COOKIES:
            book_ids = request.COOKIES['book_ids']
            counter = book_ids.split('|')
            book_count = len(set(counter))
        else:
            book_count = 0
        return render(request, 'library/dashboard.html',{'books': books, 'books_count': book_count})
    else:
        return render(request, 'library/index.html')


def afterlogin_view(request):
    return render(request, 'library/dashboard.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account successfully created!')
            return redirect('lib-login')
        context = {
            "page": "register",
            "form": form
        }
    else:
        context = {
            "page": "register",
            "form": UserRegistrationForm()
        }
    return render(request, "library/register.html", context)


@login_required
def chat(request):
    User = get_user_model()
    users = User.objects.all()
    chats = {}
    if request.method == 'GET' and 'u' in request.GET:
        # chats = chatMessages.objects.filter(Q(user_from=request.user.id & user_to=request.GET['u']) | Q(user_from=request.GET['u'] & user_to=request.user.id))
        chats = chatMessages.objects.filter(
            Q(user_from=request.user.id, user_to=request.GET['u']) | Q(user_from=request.GET['u'],
                                                                       user_to=request.user.id))
        chats = chats.order_by('date_created')
    context = {
        "page": "home",
        "users": users,
        "chats": chats,
        "chat_id": int(request.GET['u'] if request.method == 'GET' and 'u' in request.GET else 0)
    }
    print(request.GET['u'] if request.method == 'GET' and 'u' in request.GET else 0)
    return render(request, "library/chat.html", context)


@login_required
def get_messages(request):
    chats = chatMessages.objects.filter(Q(id__gt=request.POST['last_id']),
                                        Q(user_from=request.user.id, user_to=request.POST['chat_id']) | Q(
                                            user_from=request.POST['chat_id'], user_to=request.user.id))
    new_msgs = []
    for chat in list(chats):
        data = {}
        data['id'] = chat.id
        data['user_from'] = chat.user_from.id
        data['user_to'] = chat.user_to.id
        data['message'] = chat.message
        data['date_created'] = chat.date_created.strftime("%b-%d-%Y %H:%M")
        print(data)
        new_msgs.append(data)
    return HttpResponse(json.dumps(new_msgs), content_type="application/json")


@login_required
def send_chat(request):
    resp = {}
    User = get_user_model()
    if request.method == 'POST':
        post = request.POST

        u_from = UserModel.objects.get(id=post['user_from'])
        u_to = UserModel.objects.get(id=post['user_to'])
        insert = chatMessages(user_from=u_from, user_to=u_to, message=post['message'])
        try:
            insert.save()
            resp['status'] = 'success'
        except Exception as ex:
            resp['status'] = 'failed'
            resp['mesg'] = ex
    else:
        resp['status'] = 'failed'

    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def lib_view(request):
    books =models.Books.objects.all()
    if 'book_ids' in request.COOKIES:
        book_ids = request.COOKIES['book_ids']
        counter=book_ids.split('|')
        book_count=len(set(counter))
    else:
        book_count=0
    return render(request, 'library/lib_home.html',{'books':books,'book_count':book_count})


def add_to_wishlist(request,pk):
    books=models.Books.objects.all()

    #for cart counter, fetching products ids added by customer from cookies
    if 'book_ids' in request.COOKIES:
        book_ids = request.COOKIES['book_ids']
        counter=book_ids.split('|')
        book_count=len(set(counter))
    else:
        book_count=1

    response = render(request, 'library/ondex.html',{'books':books,'book_count':book_count})


    if 'book_ids' in request.COOKIES:
        book_ids = request.COOKIES['book_ids']
        if book_ids=="":
            book_ids=str(pk)
        else:
            book_ids=book_ids+"|"+str(pk)
        response.set_cookie('book_ids', book_ids)
    else:
        response.set_cookie('book_ids', pk)

    book=models.Books.objects.get(id=pk)
    messages.info(request, book.title + ' added to wishlist successfully!')

    return response


@login_required
def borrowed_books_view(request, book_to=None):
    books=models.IssueBook.objects.filter(book_to=book_to)
    return render(request,'library/borrowed_book.html',{'books':books})    


@login_required
def fines(request):
    books = models.IssueBook.objects.all()
    return render(request,'library/fines.html',{'books':books})


@login_required
def my_profile_view(request):
    Students = models.Students.objects.all()
    context = {
        "page": "profile",

    }
    return render(request, "library/profile.html", context)


def wishlist(request):
    if 'book_ids' in request.COOKIES:
        book_ids = request.COOKIES['book_ids']
        counter=book_ids.split('|')
        book_count=len(set(counter))
    else:
        book_count=0

    book=None
    if 'book_ids' in request.COOKIES:
        book_ids = request.COOKIES['book_ids']
        if book_ids != "":
            book_id_in_wishlist=book_ids.split('|')
            book =models.Books.objects.all().filter(id__in = book_id_in_wishlist)
    return render(request,'library/wishlist.html',{'books':book,'book_count':book_count})


@login_required
def remove_book(request,pk):
    if 'book_ids' in request.COOKIES:
        book_ids = request.COOKIES['book_ids']
        counter=book_ids.split('|')
        book_count=len(set(counter))
    else:
        book_count=0

    if 'book_ids' in request.COOKIES:
        book_ids = request.COOKIES['book_ids']
        book_id_in_wishlist=book_ids.split('|')
        book_id_in_wishlist=list(set(book_id_in_wishlist))
        book_id_in_wishlist.remove(str(pk))
        books=models.Books.objects.all().filter(id__in = book_id_in_wishlist)
        value=""
        for i in range(len(book_id_in_wishlist)):
            if i==0:
                value=value+book_id_in_wishlist[0]
            else:
                value=value+"|"+book_id_in_wishlist[i]
        response = render(request, 'library/wishlist.html',{'books':books,'book_count':book_count,'redirect_to' : request.GET['next_page']})
        if value=="":
            response.delete_cookie('book_ids')
        response.set_cookie('book_ids',value)
        return response


@login_required
def search_view(request):
    query = request.GET['query']
    books=models.Books.objects.all().filter(title__icontains=query)
    if 'book_ids' in request.COOKIES:
        book_ids = request.COOKIES['book_ids']
        counter=book_ids.split('|')
        book_count_in_cart=len(set(counter))
    else:
        book_count_in_cart=0
    word="Searched Result :"
    if request.user.is_authenticated:
        return render(request,'library/lib_home.html',{'books':books,'word':word,'book_count':book_count_in_cart, 'search_text': query})
    return render(request,'library/ondex.html',{'books':books,'word':word,'book_count':book_count_in_cart, 'search_text': query})


def requests(request,id):
    book = Books.objects.get(id=id)

    return render(request, 'library/request_address.html', {'book':book,'book_id':id,'title':'Request a book'})

def request_book(request,id):
    user_id = request.user.id
    book = Books.objects.get(id=id)
    if book.status == 'available':
        book.status == 'unavailable'
        book.save()
    user = User.objects.get(id=user_id)
    requested_book = Request.objects.create(user=user, book=book, date_requested=datetime.datetime.now())
    requested_book.save()
    messages.info(request, ("Book was requested succesfull. wait for librarian to issue book"))

    return render(request,'library/dashboard.html')


def return_book(request,id):
    book = models.Request.objects.get(id=id)

    return render(request, 'library/returning_book.html', {'book':book,'book_id':id,'title':'Return a book'})

def return_book_view(request,id):
    user_id = request.user.id
    book = models.Request.objects.get(id=id)
    if book.status == 'unavailable':
        book.status == 'available'
        book.save()
    user = User.objects.get(id=user_id)
    return_book = models.Returns.objects.create(user=user, book=book, date_returned=datetime.datetime.now())
    return_book.save()
    messages.info(request, ("RETURN request for book was successfully  sent. wait for librarian to issue book"))

    return render(request,'library/return_success.html')


def notification(request):
    return render(request, 'library/dashboard.html', {
        'room_name': "broadcast"
    })


from asgiref.sync import async_to_sync
def test(request):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notification_broadcast",
        {
            'type': 'send_notification',
            'message': json.dumps("Notification")
        }
    )
    return HttpResponse("Done")


