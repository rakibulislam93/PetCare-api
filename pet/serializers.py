from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.serializers import UserRegistrationSerializer,ProfileSerializer

from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class PetSerializer(serializers.ModelSerializer):
    added_by = serializers.StringRelatedField()  
    class Meta : 
        model = models.PetModel
        fields = '__all__'

class AdoptionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.AdoptionModel
        fields = '__all__'
        read_only_fields = ['user']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['id','name']

class ReviewSerializer(serializers.ModelSerializer):
    
    reviewer = ProfileSerializer(source='reviewer.profile',read_only=True)
    class Meta:
        model = models.Review
        fields = '__all__'
        