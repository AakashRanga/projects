from django.db import models

class Manufacturing_team(models.Model):

    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=200)
    phone = models.BigIntegerField()
    address = models.CharField(max_length=255)
