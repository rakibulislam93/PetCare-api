from rest_framework import serializers
from django.contrib.auth.models import User
from . import models


# User Registration part
class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password','confirm_password']
    
    def save(self):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        password1 = self.validated_data['password']
        password2 = self.validated_data['confirm_password']

        if password1 != password2 :
            raise serializers.ValidationError({'error':"Two Password Doesn't Match"})
        
        if User.objects.filter(email=email):
            raise serializers.ValidationError({'error':"Email Already Exists"})
        
        account = User(username=username,email=email,first_name=first_name,last_name=last_name)
        account.set_password(password1)
        account.is_active = False
        account.save()
        return account

    
    
# User login Serializer part
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    

# User password change part
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


# User profile part
class ProfileSerializer(serializers.ModelSerializer):
    balance = serializers.DecimalField(max_digits=12, decimal_places=2, default=0)
    user = serializers.StringRelatedField()
    class Meta:
        model = models.Profile
        fields = '__all__'
    
# User Deposite part
class DepositeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Deposite
        fields = ['user','amount']
        
        extra_kwargs = {
            'user': {'read_only': True}  # Make user field read-only
        }


# User can change his profile
class ProfileUpdateSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(required=False)

    class Meta : 
        model = User
        fields = ['username','first_name','last_name','email','profile_image']

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username',instance.username)
        instance.first_name = validated_data.get('first_name',instance.first_name)
        instance.last_name = validated_data.get('last_name',instance.last_name)
        instance.email = validated_data.get('email',instance.email)

        profile_image = validated_data.get('profile_image')

        if profile_image:
            if hasattr(instance,'profile'):
                instance.profile.profile_image = profile_image
                instance.profile.save()
        
        instance.save()

        return instance
    


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contact
        fields = '__all__'