from tkinter.tix import Tree
from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from datetime import datetime, timedelta
from datetime import date
from django.db import models
from datetime import datetime
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import MINUTES, PeriodicTask, CrontabSchedule, PeriodicTasks
import json


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=50)
    is_login = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'


class chatMessages(models.Model):
    user_from = models.ForeignKey(User,
                                  on_delete=models.CASCADE, related_name="+")
    user_to = models.ForeignKey(User,
                                on_delete=models.CASCADE, related_name="+")
    message = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.message

    class Meta:
        verbose_name_plural = "Chats"


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
    Cover = models.ImageField(upload_to='book_image/', null=True, blank=True)
    status = models.CharField(max_length=30, choices=(('available', 'available'), ('unavailable', 'unavailable')),
                              default='available')
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
        return self.student_id, ' ', self.first_name, ' ', self.middle_name if not self.middle_name == '' else ' ', self.Surname

    def name(self):
        return self.first_name, ' ', self.middle_name if not self.middle_name == '' else '', self.Surname

    @property
    def get_id(self):
        return self.user.id


def get_expiry():
    return datetime.today() + timedelta(days=7)


class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Books, on_delete=models.CASCADE, null=True)
    date_requested = models.DateField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, default=get_expiry)
    status = models.ForeignKey(Books, on_delete=models.CASCADE, null=True, related_name="+")

    def __str__(self):
        return self.book


class Returns(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Request, on_delete=models.CASCADE, null=True)
    date_returned = models.DateField(auto_now_add=True)
    status = models.ForeignKey(Books, on_delete=models.CASCADE, null=True, related_name="+")

    def __str__(self):
        return self.book
    class Meta:
        verbose_name_plural = "Return"


@property
def fine_calc(self, days):
    if self.return_date + timedelta(0<=days<=3):
        return "5000"

    elif self.return_date + timedelta(days>=3):
        return "10,000"

    else:
        return "Not yet Fine"


class IssueBook(models.Model):
    book_to = models.ForeignKey(User,
                                on_delete=models.CASCADE, related_name="+")
    issue_book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name="+")
    Issuing_date = models.ForeignKey(Request, on_delete=models.CASCADE, related_name="+", null=True)
    status = models.CharField(max_length=2, choices=(('1', 'Available'), ('2', 'Unavailable')), null=True, default=1)
    date_created = models.DateTimeField(auto_now_add=True, null=Tree)
    return_date = models.DateTimeField(null=True, default=get_expiry)
    Fine = fine_calc

    class Meta:

        verbose_name_plural = "Issue a book to a student "

    def __str__(self):
        return str(f"{self.issue_book}, {self.Fine}, {self.book_to}, {self.status}")


class BroadcastNotification(models.Model):
    notification_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    message = models.TextField()
    broadcast_on = models.DateTimeField()
    sent = models.BooleanField(default=False)

    class Meta:
        ordering = ['-broadcast_on']

@receiver(post_save, sender=BroadcastNotification)
def notification_handler(sender, instance, created, **kwargs):
    # call group_send function directly to send notificatoions or you can create a dynamic task in celery beat
    if created:
        schedule, created = CrontabSchedule.objects.get_or_create(hour = instance.broadcast_on.hour, minute = instance.broadcast_on.minute, day_of_month = instance.broadcast_on.day, month_of_year = instance.broadcast_on.month)
        task = PeriodicTask.objects.create(crontab=schedule, name="broadcast-notification-"+str(instance.id), task="notifications_app.tasks.broadcast_notification", args=json.dumps((instance.id,)))


