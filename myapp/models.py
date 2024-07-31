from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class Login(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
#
class Doctor(models.Model):
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE)
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    photo = models.CharField(max_length=480)
    email = models.CharField(max_length=10)
    address = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    pincode = models.CharField(max_length=30)

class Patient(models.Model):
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE)
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    photo = models.CharField(max_length=480)
    email = models.CharField(max_length=10)
    address = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    pincode = models.CharField(max_length=30)

