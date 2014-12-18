from django.db import models

# Create your models here.


class Company(models.Model):
    RegisteredNumber = models.CharField(max_length=8, primary_key=True)
    Name = models.CharField(max_length=500)
    Turnover = models.IntegerField(default=0)
    Profit = models.IntegerField(default=0)
    Employees = models.IntegerField(default=0)
    SIC = models.CharField(max_length=6)
    AddressLine1 = models.CharField(max_length=500)
    AddressLine2 = models.CharField(max_length=500)
    AddressLine3 = models.CharField(max_length=500)
    AddressLine4 = models.CharField(max_length=500)
    AddressLine5 = models.CharField(max_length=500)
    Town = models.CharField(max_length=100)
    County = models.CharField(max_length=50)
    Postcode = models.CharField(max_length=10)

