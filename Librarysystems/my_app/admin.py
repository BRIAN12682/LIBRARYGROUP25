#from django.contrib import admin

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class Admin(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_publisher = models.BooleanField(default=False)
    is_librarian = models.BooleanField(default=False)

    class Meta:
        swappable = 'AUTH_USER MODEL'


class Books(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    pdf = models.FileField(upload_to='uploads/pdfs/', null=True, blank=True)
    cover = models.ImageField(upload_to='uploads/cover/', null=True, blank=True)

    def __str__(self):
        return self.title


'''    def delete(self, *args, **kwargs ):
        self.pdf.delete()
        self.cover.delete()
        super().delete(*args, **kwargs)
'''

# Register your models here.
