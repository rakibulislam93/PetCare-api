from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from . import models
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView

from rest_framework import viewsets,permissions
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework import generics


# User can update his profile if his an authenticated and requested user
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print('User : ',request.user)
        print('Auth : ',request.auth)
        
        return obj == request.user



# ApiView For User Registration..........
class UserRegistrationApiView(APIView):
    serializer_class = serializers.UserRegistrationSerializer
    def post(self,request):
        data = request.data        
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            user = serializer.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            confirm_link = f"http://127.0.0.1:8000/accounts/activate/{uid}/{token}"
            email_subject = "Confirm Your Email"
            email_body = render_to_string("confirm_email.html",{
                'confirm_link':confirm_link,
            })
            email = EmailMultiAlternatives(email_subject,to=[user.email])
            email.attach_alternative(email_body,"text/html")
            email.send()

            return Response({"messages":"Check your mail for confirmation"})
        
        return Response(serializer.errors)


# User Activate function...........
def activate(request,uid64,token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return redirect('register')
    

# User Login part
class UserLoginApiView(APIView):
    serializer_class = serializers.UserLoginSerializer  
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username,password=password)
            if user:
                token,created = Token.objects.get_or_create(user=user)

                login(request,user)
                return Response({'messages':"Login successfull",'token':token.key,'user_id':user.id})
            else:
                return Response({'error':"Invalid Credentials"})
        
        else:
            return Response(serializer.errors)
        


# User Logout part
class UserLogoutView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    def post(self,request):
        
        if request.user.is_authenticated:
            
            request.user.auth_token.delete()
            logout(request)        
            return Response({'message':'Log out successfull'})
        return Response({"detail": "User not authenticated."}, status=400)    




class ChangePassword(GenericAPIView):
    serializer_class = serializers.ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    def put(self, request):
        password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        # Check if password fields are provided
        if not password or not new_password:
            return Response({'error': 'Both password and new_password fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        # Check if the old password matches
        if not user.check_password(password):
            return Response({'error': 'Old password does not match.'}, status=status.HTTP_400_BAD_REQUEST)

        # Set the new password
        user.set_password(new_password)
        user.save()

        return Response({'success': 'Password changed successfully.'}, status=status.HTTP_200_OK)

    



class ProfileApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes=[TokenAuthentication,SessionAuthentication]

    def get(self,request):
        profile = models.Profile.objects.filter(user=request.user).first()
        if profile:
            serializer = serializers.ProfileSerializer(profile,context={'request':request})
            return Response(serializer.data)
        return Response({'error':'Profile not found'},status=status.HTTP_400_BAD_REQUEST)
    



class DepositeApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    serializer_class = serializers.DepositeSerializer
    
    def post(self,request):
        data = request.data
        user_id = request.user.id
        serializer = self.serializer_class(data=data)       
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            profile = models.Profile.objects.filter(user_id=user_id).first()
            print(profile)
            if profile:
                profile.balance += amount
                profile.save()
                return Response({'success':'Deposite successfull'},status=status.HTTP_201_CREATED)
            
            return Response({'error':'Invalid profile'},status=status.HTTP_400_BAD_REQUEST)       
        return Response(serializer.errors)


class ProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.ProfileUpdateSerializer
    permission_classes = [IsOwner]
    authentication_classes=[TokenAuthentication,SessionAuthentication]
    lookup_field = 'pk'
    
    def get_object(self):
        
        obj = super().get_object()
        return obj


# Contact model er kaj start
class ContactApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    serializer_class = serializers.ContactSerializer
    
    def post(self,request):
        data = request.data 

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            contact = serializer.save()
            user_email = request.user.email
            print(user_email)
            subject = f"New Contact Us Message from {contact.name}"
            message_body = f"""
            You have received a new message from the Contact Us form.

            Details:
            ---------
            Name: {contact.name}
            Email: {user_email}

            Message:
            --------
            {contact.massage}

            Thank you!
            """
            send_mail(
                subject, 
                message_body, 
                user_email, 
                ['rakibulislamarif793@gmail.com'], 
            )
            return Response({'success':'Message sent successful,,waiting for response'})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)