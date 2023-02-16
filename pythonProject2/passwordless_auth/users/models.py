from django.db import models

class user_approve(models.Model):
    name = models.CharField(max_length=255, null=True, default=None)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=200)
    approved = models.BooleanField(default=False)
    status = models.CharField(max_length=255,default="Not Approved")
    boolean = models.BooleanField(default=False)

class invaded_acc(models.Model):
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=200)

class users_details(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=200)
    phone = models.BigIntegerField()
    f1 = models.CharField(max_length=255)
    f2 = models.CharField(max_length=255)
    f3 = models.CharField(max_length=255)
    f4 = models.CharField(max_length=255)
    f5 = models.CharField(max_length=255)
    login_attempts = models.IntegerField(default=0)
    pattern = models.CharField(max_length=50)
    a1 = models.CharField(max_length=255, default=0)
    a2 = models.CharField(max_length=255, default=0)
    a3 = models.CharField(max_length=255, default=0)
    a4 = models.CharField(max_length=255, default=0)
    a5 = models.CharField(max_length=255, default=0)
    approved = models.BooleanField('Approved',default=False)
    admin_status = models.BooleanField(default=False)
    secure = models.BooleanField(default=True)

class LoginAttempt(models.Model):
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    login_attempts = models.IntegerField(default=0)
    pattern = models.CharField(max_length=50)

