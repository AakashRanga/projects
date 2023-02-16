from django.contrib import admin
from django.contrib.auth.models import Group
from .models import users_details
# Register your models here.

@admin.register(users_details)
class EventAdmin(admin.ModelAdmin):
    fields = ('approved',)