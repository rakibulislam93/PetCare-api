from django.contrib import admin
from . import models
# Register your models here.


class CategoryModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = ['id','name']
    list_display_links = ['id','name']

class PetModelAdmin(admin.ModelAdmin):
    list_display = ['id','name','price','image','age','added_by','category']
    list_display_links = ['id','name']



admin.site.register(models.PetModel,PetModelAdmin)
admin.site.register(models.AdoptionModel)
admin.site.register(models.Category,CategoryModelAdmin)
admin.site.register(models.Review)