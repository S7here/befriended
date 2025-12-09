from django.db import models

# Create your models here.
class MasterCollege(models.Model):
    counselling_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200,null=True,blank=True)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    students_count = models.IntegerField()
    class Meta:
        db_table = 'college"."master_college'