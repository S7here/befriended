import uuid
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser


class College(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField('users.CustomUser', on_delete=models.CASCADE, null=True,blank=True)
    department = models.CharField(max_length=255)
    counselling_number = models.CharField(max_length=255)
    application_no = models.CharField(max_length=100, blank=True, null=True)
    master_college = models.ForeignKey("college.MasterCollege",
                                       on_delete=models.CASCADE,
                                       null=True,        # allow empty foreign key for existing rows
                                       blank=True,
                                       related_name="students")
    class Meta:
        db_table = 'users"."college'

    def __str__(self):
        return f"{self.master_college.name if self.master_college else 'College'} - {self.department}"



class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
   
    full_name = models.CharField(max_length=200,blank=True,null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    age = models.PositiveIntegerField()
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True)
    allotment_pdf = models.FileField(upload_to='allotments/', blank=True, null=True)

    is_verified = models.BooleanField(default=False)

    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    
    class Meta:
        db_table = 'users"."custom_user'


    def __str__(self):
        return self.username
