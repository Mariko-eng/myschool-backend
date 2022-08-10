from unicodedata import category
from django.db import models
from django.contrib.auth.models import User,Group

#Django itself uses Abstract User;
#You can override the functions like createuser, createsuperuser, etc
# Eg if u want to login with phone number and password 

class Userprofile(models.Model):
    MALE = "Male"
    FEMALE = "female"
    OTHER = "other"

    GENDER_CHOICES = (
          (MALE, 'Male'),
          (FEMALE, 'Female'),
          (OTHER, 'Other'),
      )

    NATIONAL = "national"
    DRIVING = "driving permit"
    PASSPORT = "passport"

    INDENTIFICATION_CHOICES = [
        (NATIONAL, "national"),
        (DRIVING, "driving_permit"),
        (PASSPORT, "passport")
      ]
    user = models.OneToOneField(User,related_name = "profile",null = True,on_delete=models.SET_NULL)
    othername = models.CharField(max_length=225,null=True, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES,max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=50,null=True, blank=True)
    address = models.CharField(max_length=225, null=True, blank=True)
    idType = models.CharField(choices=INDENTIFICATION_CHOICES,max_length=50, blank=True, null=True)
    idDetails = models.CharField(max_length=50,null=True, blank=True)
    dob = models.DateField(blank=True)
    profession =models.CharField(max_length=225,null=True, blank=True)
    education_info = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User,null = True,on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True,null=True, blank=True)

class GroupCategory(models.Model):
  name = models.CharField(max_length=225)
  groups = models.ManyToManyField(Group,related_name = "category")