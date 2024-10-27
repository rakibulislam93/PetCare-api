from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    balance = models.DecimalField(max_digits=12,decimal_places=2,default=0)
    
    profile_image = models.URLField(max_length=200,null=True,blank=True)
    
    def __str__(self):
        return f'{self.user.username} ---> total balance {self.balance}'


class Deposite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deposits')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} deposits ---> {self.amount} '
    


class Contact(models.Model):
    name = models.CharField(max_length=50)
    massage = models.TextField()

    def __str__(self):
        return f'{self.massage} by {self.name}'
    
