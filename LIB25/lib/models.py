from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from datetime import date


class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    gender = models.CharField(max_length=50)
    is_login = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'


class chatMessages(models.Model):
    user_from = models.ForeignKey(User,
        on_delete=models.CASCADE,related_name="+")
    user_to = models.ForeignKey(User,
        on_delete=models.CASCADE,related_name="+")
    message = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.message


# Create your models here.
class Area(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=2, choices=(('1', 'Active'), ('2', 'Inactive')), default=1)
    delete_flag = models.IntegerField(default=0)
    date_added = models.DateTimeField(default=timezone.now)
    date_created = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Areas"

    def __str__(self):
        return str(f"{self.name}")


class SubArea(models.Model):
    category = models.ForeignKey(Area, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=2, choices=(('1', 'Active'), ('2', 'Inactive')), default=1)
    delete_flag = models.IntegerField(default=0)
    date_added = models.DateTimeField(default=timezone.now)
    date_created = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = " Sub Areas"

    def __str__(self):
        return str(f"{self.category} - {self.name}")


class Books(models.Model):
    editable_list = ['__all__']
    sub_area = models.ForeignKey(SubArea, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    author = models.TextField(blank=True, null=True)
    publisher = models.CharField(max_length=250)
    publication_date = models.DateTimeField()
    Cover = models.ImageField(upload_to='book_image/',null=True,blank=True)
    status = models.CharField(max_length=30, choices=(('available', 'available'), ('unavailable', 'unavailable')), default ='available')
    delete_flag = models.IntegerField(default=0)
    date_added = models.DateTimeField(default=timezone.now)
    date_created = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "List of Books"

    def __str__(self):
        return str(f"{self.isbn} - {self.title}")


class Students(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    search_fields = ("student_id", "first_name", "middle_name", "Surname")
    list_filter = ['student_id']
    list_display = ['__all__']
    student_id = models.CharField(max_length=250)
    registration_number = models.CharField(max_length=250)
    first_name = models.CharField(max_length=250)
    middle_name = models.TextField(max_length=250, blank=True, null=True)
    Surname = models.CharField(max_length=250)
    gender = models.CharField(max_length=20, choices=(('Male', 'Male'), ('Female', 'Female')), default='Male')
    contact = models.CharField(max_length=250)
    email = models.CharField(max_length=40)
    address = models.CharField(max_length=250)
    profile_pic = models.ImageField(upload_to='profile_pic/CustomerProfilePic/', null=True, blank=True)
    mobile = models.CharField(max_length=20, null=False)
    College = models.CharField(max_length=250, blank=True, null=True)
    course = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(max_length=15, choices=(('Active', 'Active'), ('Inactive', 'Inactive')), default=1)
    delete_flag = models.IntegerField(default=0)
    date_added = models.DateTimeField(default=timezone.now)
    date_created = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Students"

    def __str__(self):
        return self.student_id, ' ',self.first_name, ' ',self.middle_name if not self.middle_name == '' else' ', self.Surname

    def name(self):
        return self.first_name, ' ',self.middle_name if not self.middle_name == '' else '', self.Surname

    @property
    def get_id(self):
        return self.user.id


def get_expiry():
    return datetime.today() + timedelta(days=7)


class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Books, on_delete=models.CASCADE, null=True)
    date_requested = models.DateField(auto_now_add=True)
    return_date=models.DateTimeField(null=True)
    status = models.ForeignKey(Books, on_delete=models.CASCADE, null=True,related_name="+")

    def __str__(self):
        return  self.book


class IssueBook(models.Model):
    book_to = models.ForeignKey(User,
                                on_delete=models.CASCADE, related_name="+")
    issue_book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name="+")
    Issuing_date = models.user_to = models.ForeignKey(Request,on_delete=models.CASCADE, related_name="+")
    return_date = models.ForeignKey(Request, on_delete=models.CASCADE, null=True, related_name="+")
    status = models.CharField(max_length=2, choices=(('1', 'Available'), ('2', 'Unavailable')), default=1)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Issue a book to a student"

    def __str__(self):
        return str(f"{self.issue_book}")


@property
def days_till_fine(self):
    day = self.IssueBook.return_date - date.today()
    days = str(day).split(", ", 1)[0]
    return days


def fine_calc(self, days_till_fine):
    if abs(int(days_till_fine)) > 3:
        return 5000
    if abs(int(days_till_fine)) > 10:
        return 10,000
    else:
        return "No fine yet"


class FinedStudents(models.Model):
    book_to = models.ForeignKey(IssueBook,
                                on_delete=models.CASCADE, related_name="book_to+")
    Issued_book = models.ForeignKey(IssueBook, on_delete=models.CASCADE, related_name="Issued_book+")
    Issuing_date = models.ForeignKey(IssueBook, on_delete=models.CASCADE, related_name="Issuing_date+")
    return_date = models.DateField()
    days_till_fine = days_till_fine
    Fine = fine_calc
    status = models.CharField(max_length=50)
    date_created = models.DateTimeField()

    class Meta:
        verbose_name_plural = "Fines"

    def __str__(self):
        return str(f"{self.Issued_book}, {self.Fine}, {self.book_to}, {self.status}")




