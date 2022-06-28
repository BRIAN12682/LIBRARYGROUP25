from django.db import models

# Create your models here.
class Students(models.Model):
    name= models.CharField(max_length=250)
    email= models.CharField(max_length=250)
    def __str__(self):
        return self.name


class Books(models.Model):
    title=models.CharField(max_length=250)
    Author=models.CharField(max_length=250)
    publication_date=models.DateTimeField('date published')
    subject_area=models.CharField(max_length=250)
    def __str__(self):
        return self.title, self.Author, self.publication_date, self.subject_area

