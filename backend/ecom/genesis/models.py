from django.db import models

# Create your models here.
class Users(models.Model):
    fullname =models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=20)