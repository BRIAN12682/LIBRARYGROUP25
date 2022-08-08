from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import chatMessages, Books, Students,Request
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
        books = models.Books.objects.all()
        if 'book_ids' in request.COOKIES:
            book_ids = request.COOKIES['book_ids']
            counter = book_ids.split('|')
            book_count_in_cart = len(set(counter))
        else:
            book_count_in_cart = 0
        return render(request, 'library/dashboard.html',{'books': books, 'books_count_in_cart': book_count_in_cart})
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


def dashboard(request):
    books=models.Books.objects.all()
    if request.user.is_authenticated:
        return render(request, 'library/dashboard.html',{'books':books})
    return render(request,'library/index.html')


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
    return render(request, "library/home.html", context)


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
        book_count_in_cart=len(set(counter))
    else:
        book_count_in_cart=0
    return render(request, 'library/customer_home.html',{'books':books,'book_count_in_cart':book_count_in_cart})


def add_to_cart_view(request,pk):
    books=models.Books.objects.all()

    #for cart counter, fetching products ids added by customer from cookies
    if 'book_ids' in request.COOKIES:
        book_ids = request.COOKIES['book_ids']
        counter=book_ids.split('|')
        book_count_in_cart=len(set(counter))
    else:
        book_count_in_cart=1

    response = render(request, 'library/ondex.html',{'books':books,'product_count_in_cart':book_count_in_cart})


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
    messages.info(request, book.title + ' added to cart successfully!')

    return response


@login_required
def books_view(request):
    books=models.Books.objects.all()
    return render(request,'ecom/admin_products.html',{'products':books})

@login_required
def my_profile_view(request):
    student= models.Students.objects.get(id=pk)
    return render(request,'library/my_profile.html',{'student':student})


@login_required
def edit_profile_view(request):
    student=models.Students.objects.get(user_id=request.user.id)
    user=models.User.objects.get(id=student.user_id)
    userForm=forms.UserRegistrationForm(instance=user)
    studentForm=forms.StudentForm(request.FILES,instance=student)
    mydict={'userForm':userForm,'customerForm':studentForm}
    if request.method=='POST':
        userForm=forms.UserRegistrationForm(request.POST,instance=user)
        studentForm=forms.StudentForm(request.POST,instance=student)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            studentForm.save()
            return HttpResponseRedirect('my-profile')
    return render(request,'library/edit_profile.html',context=mydict)


def cart_view(request):
    if 'book_ids' in request.COOKIES:
        book_ids = request.COOKIES['book_ids']
        counter=book_ids.split('|')
        book_count_in_cart=len(set(counter))
    else:
        book_count_in_cart=0

    book=None
    if 'book_ids' in request.COOKIES:
        book_ids = request.COOKIES['book_ids']
        if book_ids != "":
            book_id_in_cart=book_ids.split('|')
            book =models.Books.objects.all().filter(id__in = book_id_in_cart)
    return render(request,'library/wishlist.html',{'books':book,'product_count_in_cart':book_count_in_cart})


@login_required
def remove_from_cart_view(request,pk):
    if 'book_ids' in request.COOKIES:
        book_ids = request.COOKIES['book_ids']
        counter=book_ids.split('|')
        book_count_in_cart=len(set(counter))
    else:
        book_count_in_cart=0

    if 'book_ids' in request.COOKIES:
        book_ids = request.COOKIES['book_ids']
        book_id_in_cart=book_ids.split('|')
        book_id_in_cart=list(set(book_id_in_cart))
        book_id_in_cart.remove(str(pk))
        books=models.Books.objects.all().filter(id__in = book_id_in_cart)
        value=""
        for i in range(len(book_id_in_cart)):
            if i==0:
                value=value+book_id_in_cart[0]
            else:
                value=value+"|"+book_id_in_cart[i]
        response = render(request, 'library/wishlist.html',{'books':books,'book_count_in_cart':book_count_in_cart,'redirect_to' : request.GET['next_page']})
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
        return render(request,'library/customer_home.html',{'books':books,'word':word,'book_count_in_cart':book_count_in_cart, 'search_text': query})
    return render(request,'library/ondex.html',{'books':books,'word':word,'book_count_in_cart':book_count_in_cart, 'search_text': query})


@login_required
def my_request_view(request):
    student = models.Students.objects.get(user_id=request.user.id)
    requests = models.Request.objects.all().filter(student_id=student)
    requested_books = []
    for request in requests:
        requested_book = models.Books.objects.all().filter(id=request.product.id)
        requested_books.append(requested_book)

    return render(request, 'library/my_request.html', {'data': zip(requested_books, requests)})


@login_required
def student_info(request):
    book_in_cart=False
    if 'book_ids' in request.COOKIES:
        book_ids = request.COOKIES['book_ids']
        if book_ids != "":
            book_in_cart=True
    if 'book_ids' in request.COOKIES:
        book_ids = request.COOKIES['book_ids']
        counter=book_ids.split('|')
        book_count_in_cart=len(set(counter))
    else:
        book_count_in_cart=0

    form = forms.UserRegistrationForm()
    if request.method == 'POST':
        form = forms.UserRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['college']
            college=form.cleaned_data['course']
            course = form.cleaned_data['course']
            response = render(request, 'library/request1.html')
            response.set_cookie('email',email)
            response.set_cookie('college',college)
            response.set_cookie('course',course)
            return response
    return render(request,'library/customer_address.html',{'form':form,'book_in_cart':book_in_cart,'book_count_in_cart':book_count_in_cart})






@login_required
def view(request):
    first_name=models.Students.objects.filter(user_id=request.user.id)
    issue_book=models.IssuedBook.objects.filter(student_id=first_name[0].student_id)

    list1=[]

    list2=[]
    for issueB in issue_book:
        books=models.Books.objects.filter(status=issueB.status)
        for book in books:
            t=(request.user,first_name[0].student_id,first_name[0].adress,book.title,book.author)
            list1.append(t)
        issdate=str(issueB.Issuing_date.day)+'-'+str(issueB.Issuing_date.month)+'-'+str(issueB.Issuing_date.year)
        expdate=str(issueB.return_date.day)+'-'+str(issueB.return_date.month)+'-'+str(issueB.return_date.year)
        #fine calculation
        days=(datetime.date.today()-issueB.Issuing_date)
        print(datetime.date.today())
        d=days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*10
        t=(issdate,expdate,fine)
        list2.append(t)

    return render(request,'library/viewborrowedbook.html',{'list1':list1,'list2':list2})


def requests(request,id):
    book = Books.objects.get(id=id)

    return render(request, 'library/customer_address.html', {'book':book,'book_id':id,'title':'Request a book'})

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


