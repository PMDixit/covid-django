from enum import auto, unique
from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey

# Create your models here.
class Doctor(models.Model):
    d_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=30)
    gender=models.CharField(max_length=2)
    phone_no=models.BigIntegerField()
    specialization=models.CharField(max_length=30)
    password=models.CharField(max_length=200)

class Ward(models.Model):
    ward_id=models.AutoField(primary_key=True)
    ward_type=models.CharField(max_length=30)
    no_of_beds=models.IntegerField()
    price=models.IntegerField()

class Patient(models.Model):
    p_id=models.AutoField(primary_key=True)
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    gender=models.CharField(max_length=2)
    phone_no=models.BigIntegerField()
    address=models.CharField(max_length=100)
    discription=models.TextField()
    status=models.CharField(max_length=20,default="Active")
    ward=models.IntegerField(null=True)
    Date_of_Admit=models.DateTimeField()
    Date_of_Discharge=models.DateTimeField(null=True)
    password=models.CharField(max_length=200)

class Recptionalist(models.Model):
    r_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=30)
    password=models.CharField(max_length=200)

class Medicine(models.Model):
    m_id=models.AutoField(primary_key=True)
    med_name=models.CharField(max_length=30)
    mfd_company=models.CharField(max_length=30)

class Service(models.Model):
    ser_id=models.AutoField(primary_key=True)
    ser_name=models.CharField(max_length=30)
    price=models.IntegerField()

class Prescribed_to(models.Model):
    m=models.IntegerField()
    p=models.IntegerField()
    class Meta:
        unique_together = ('m', 'p')

class Treats(models.Model):
    d=models.IntegerField()
    p=models.IntegerField()
    class Meta:
        unique_together = ('d', 'p')

class Avails(models.Model):
    p=models.IntegerField()
    service=models.IntegerField()
    class Meta:
        unique_together = ('p', 'service')