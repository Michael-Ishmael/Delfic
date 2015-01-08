import json
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
    WebsiteUrl = models.CharField(max_length=200, null=True)
    Postcode = models.CharField(max_length=10)

    def to_json_obj(self):
        json_company_obj = {
            "registerednumber": self.RegisteredNumber,
            "name": self.Name,
            "address": {
                "addr1": self.AddressLine1,
                "addr2": self.AddressLine2,
                "addr3": self.AddressLine3,
                "addr4": self.AddressLine4,
                "addr5": self.AddressLine5,
                "town": self.Town,
                "county": self.County,
                "postcode": self.Postcode,
            }
        }
        return json_company_obj


class CompanySiteLink(models.Model):
    Company = models.ForeignKey(Company)
    TypeKey = models.CharField(max_length=20)
    Url = models.CharField(max_length=200)