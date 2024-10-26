from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True,blank=True)

    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

class PetModel(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.TextField()
    price = models.DecimalField(max_digits=12,decimal_places=2)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to="pet/images/")
    age = models.FloatField(null=True,blank=True)
    added_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self) -> str:
        return self.name


class AdoptionModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='adoption')
    pet = models.ForeignKey(PetModel,on_delete=models.CASCADE,related_name='adoption')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username} adopted {self.pet.name}"
    

CHOICES =({
    '⭐':'⭐',
    '⭐⭐':'⭐⭐',
    '⭐⭐⭐':'⭐⭐⭐',
    '⭐⭐⭐⭐': '⭐⭐⭐⭐',
    '⭐⭐⭐⭐⭐' : '⭐⭐⭐⭐⭐',

})


class Review(models.Model):
    pet = models.ForeignKey(PetModel,on_delete=models.CASCADE,related_name='review')
    reviewer = models.ForeignKey(User,on_delete=models.CASCADE,related_name='review')
    body = models.TextField()
    ratting = models.CharField(max_length=50,choices=CHOICES)

    def __str__(self) -> str:
        return f"{self.body} by {self.reviewer.username}"