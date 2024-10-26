from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from . import models
# Register your models here.

class CustomUserAdmin(UserAdmin):
    
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff')
    search_fields = ('username',)
    list_display_links = ['id','username']

admin.site.unregister(User)
admin.site.register(User,CustomUserAdmin)
admin.site.register(models.Deposite)
admin.site.register(models.Profile)
admin.site.register(models.Contact)