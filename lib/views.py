from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .models import chatMessages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User as UserModel
from django.db.models import Q
import json, datetime
from django.contrib.auth.models import User
from . import models, forms
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.core import serializers


def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
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


def dashboard(request):
    books=models.Books.objects.all()
    if 'book_ids' in request.COOKIES:
        book_ids = request.COOKIES['book_ids']
        counter=book_ids.split('|')
        book_count_in_wishlist=len(set(counter))
    else:
        book_count_in_wishlist=0
    if request.user.is_authenticated:
        return render(request, 'library/dashboard.html')
    return render(request,'library/index.html',{'books':books,'book_count_in_cart':book_count_in_wishlist})


@login_required
def home(request):
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


def context_data(request):
    fullpath = request.get_full_path()
    abs_uri = request.build_absolute_uri()
    abs_uri = abs_uri.split(fullpath)[0]
    context = {
        'system_host': abs_uri,
        'page_name': '',
        'page_title': '',
        'system_name': 'LIB MANAGEMENT SYS GROUP 23',
        'topbar': 'EXPLORE, EXPLOIT AND ENJOY',
        'footer': 'library management system @2022 Copyright',
    }
    return context


@login_required
def profile(request):
    context = {
        "page": "profile",
    }
    return render(request, "lib/profile.html", context)


@login_required(login_url='login')
def update_profile(request):
    customer=models.Students.objects.get(user_id=request.user.id)
    user=models.User.objects.get(id=customer.user_id)
    userForm=forms.UserRegistrationForm(instance=user)
    customerForm=forms.UserRegistrationForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'UserRegistrationForm':UserRegistrationForm}
    if request.method=='POST':
        userForm=forms.UserRegistrationForm(request.POST,instance=user)
        customerForm=forms.UserRegistrationForm(request.POST,instance=customer)
        if userForm.is_valid() and UserRegistrationForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return HttpResponseRedirect('my-profile')
    return render(request,'ecom/edit_profile.html',context=mydict)

@login_required
def update_password(request):
    context = context_data(request)
    context['page_title'] = "Update Password"
    if request.method == 'POST':
        form = forms.UpdatePasswords(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Account Password has been changed successfully")
            update_session_auth_hash(request, form.user)
            return redirect("profile-page")
        else:
            context['form'] = form
    else:
        form = forms.UpdatePasswords(request.POST)
        context['form'] = form
    return render(request, 'update_password.html', context)


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
def request_home_view(request):
    books=models.Books.objects.all()
    if 'book_name' in request.COOKIES:
        book_name = request.COOKIES['book_name']
        counter=book_name.split('|')
        book_count_in_wishlist=len(set(counter))
    else:
        book_count_in_wishlist=0
    if request.user.is_authenticated:
        return render(request, 'library/student_home.html')
    return render(request,'lib/index.html',{'products':books,'product_count_in_cart':book_count_in_wishlist})


def search_view(request):
    # whatever user write in search box we get in query
    query = request.GET['query']
    books = models.Books.objects.all().filter(name__icontains=query)
    if 'book_ids' in request.COOKIES:
        book_ids = request.COOKIES['book_ids']
        counter=book_ids.split('|')
        book_count_in_wishlist=len(set(counter))
    else:
        book_count_in_wishlist = 0

    # word variable will be shown in html when user click on search button
    word="Searched Result :"

    if request.user.is_authenticated:
        return render(request,'library/student_home.html',{'books':books,'word':word,'product_count_in_cart':book_count_in_wishlist})
    return render(request,'lib/index.html',{'books':books,'word':word,'product_count_in_cart':book_count_in_wishlist})


# any one can add product to cart, no need of signin
def add_to_wishlist_view(request,pk):
    books=models.Books.objects.all()

    #for cart counter, fetching products ids added by customer from cookies
    if 'book_ids' in request.COOKIES:
        book_ids = request.COOKIES['product_ids']
        counter=book_ids.split('|')
        book_count_in_wishlist=len(set(counter))
    else:
        book_count_in_wishlist=1

    response = render(request, 'lib/index.html',{'products':books,'product_count_in_cart':book_count_in_wishlist})

    if 'book_ids' in request.COOKIES:
        book_ids = request.COOKIES['book_ids']
        if book_ids=="":
            book_ids=str(pk)
        else:
            book_ids= book_ids+"|"+str(pk)
        response.set_cookie('book_ids', book_ids)
    else:
        response.set_cookie('book_ids', pk)

    book=models.Books.objects.get(id=pk)
    messages.info(request, book.name + ' added to cart successfully!')

    return response

# for checkout of wishlist
def wishlist_view(request):
    #for cart counter
    if 'book_ids' in request.COOKIES:
        book_ids = request.COOKIES['product_ids']
        counter= book_ids.split('|')
        book_count_in_wishlist=len(set(counter))
    else:
        book_count_in_wishlist=0

    # fetching product details from db whose id is present in cookie
    books=None
    if 'book_ids' in request.COOKIES:
        book_ids = request.COOKIES['book_ids']
        if book_ids != "":
            book_id_in_wishlist= book_ids.split('|')
            books=models.Books.objects.all().filter(id__in = book_id_in_wishlist)
    return render(request,'lib/cart.html',{'products': books,'book_count_in_wishlist':book_count_in_wishlist})


def remove_from_wishlist_view(request,pk):
    if 'book_ids' in request.COOKIES:
        book_ids = request.COOKIES['book_ids']
        counter=book_ids.split('|')
        book_count_in_wishlist=len(set(counter))
    else:
        book_count_in_wishlist=0

    # removing book id from cookie
    total=0
    if 'book_ids' in request.COOKIES:
        book_ids = request.COOKIES['product_ids']
        book_id_in_wishlist= book_ids.split('|')
        book_id_in_wishlist=list(set(book_id_in_wishlist))
        book_id_in_wishlist.remove(str(pk))
        books=models.Books.objects.all().filter(id__in = book_id_in_wishlist)
        #for total price shown in cart after removing product
        for b in books:
            total=total+1

        #  for update coookie value after removing product id in cart
        value=""
        for i in range(len(book_id_in_wishlist)):
            if i==0:
                value=value+book_id_in_wishlist[0]
            else:
                value=value+"|"+book_id_in_wishlist[i]
        response = render(request, 'lib/cart.html',{'products':books,'product_count_in_cart':book_count_in_wishlist})
        if value=="":
            response.delete_cookie('book_ids')
        response.set_cookie('book_ids',value)
        return response


@login_required
def my_request_view(request):
    student=models.Students.objects.get(user_id=request.user.student_id)
    requests=models.Request.objects.all().filter(student_id = student)
    requested_book=[]
    for request in requests:
        requested_book=models.Books.objects.all().filter(id=request.book.id)
        requested_book.append(requested_book)

    return render(request, 'lib/my_order.html',{'data':zip(requested_book,requests)})


@login_required
def update_request_view(request,pk):
    request=models.Request.objects.get(id=pk)
    RequestForm=forms.RequestForm(instance=request)
    if request.method=='POST':
        requestForm =forms.RequestForm(request.POST,instance=request)
        if requestForm.is_valid():
            requestForm.save()
            return redirect('admin-view-booking')
    return render(request,'lib/update_order.html',{'requestForm':RequestForm})


