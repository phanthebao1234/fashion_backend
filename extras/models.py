from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Address(models.Model):
    HOME = 'home'
    OFFICE = 'office'
    SCHOOL = 'school'
    ADDRESSTYPES = (
        (HOME, 'home'),
        (OFFICE, 'office'),
        (SCHOOL, 'school'),
    )
    
    lat = models.FloatField(default=0.0)
    lng = models.FloatField(default=0.0)
    isDefault = models.BooleanField(default=False)
    address = models.CharField(max_length=255, blank=False)
    phone = models.CharField(max_length=255, blank=False)    
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    addressType = models.CharField(choices=ADDRESSTYPES, max_length=10, default=HOME)
    
    def __str__(self):
        return f'{self.userId.username}/{self.addressType}/{self.address}'
    
class Extras(models.Model):
    isVerified = models.BooleanField(default=False)
    otp = models.CharField(max_length=255, blank=False)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.userId.username}|{self.id}'