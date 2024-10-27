from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets,permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models
from . import serializers
from rest_framework import filters
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from accounts.models import Profile
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
# Create your views here.

# pet---> get,post,put,delete  er jonno custom permission class
class IsAdminOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print('User',request.user)
        print('Auth : ',request.auth)
        if request.user.is_staff:
            return True
        return obj.added_by == request.user

class PetViewSet(viewsets.ModelViewSet):
    queryset = models.PetModel.objects.all()
    serializer_class = serializers.PetSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'category__name']
    
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    
    
    def get_permissions(self):
        
        if self.action in ['update','partial_update','destroy']:
            
            self.permission_classes = [IsAdminOrOwner]

        elif self.action == 'create':
            self.permission_classes = [permissions.IsAuthenticated]
        
        else:
            self.permission_classes = [permissions.AllowAny]

        return super().get_permissions()
    
    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)

# pet get,post,put,delete er kaj finish......


# akta user er add kora pet gulake filter korbo
class UserAddedPet(APIView):
    permission_classes=[permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    def get(self,request):
        user = request.user
        pet = models.PetModel.objects.filter(added_by=user)
        if pet:
            serializer = serializers.PetSerializer(pet,many=True,context={'request':request})
            return Response(serializer.data)
        return Response({'error':'You have no added pet'})


# category view er kaj shuru
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name__icontains']

    # user can only get category..admin can--> CRUD operation
    def get_permissions(self):
        if self.request.method in ['POST','PUT','PATCH','DELETE']:
            return [permissions.IsAdminUser()]
        
        return super().get_permissions()

# category view er kaj shesh 



# Addoption view er kaj start..............
class AdoptionViewSet(viewsets.ModelViewSet):
    queryset = models.AdoptionModel.objects.all()
    serializer_class = serializers.AdoptionSerializer
    # permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication,TokenAuthentication]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # 'list'  'retrieve' action sobai dekhte parbe
            self.permission_classes = [permissions.AllowAny]
        else:
            # shudu login kora user ra baki kaj korte parbe
            self.permission_classes = [permissions.IsAuthenticated]

        return super().get_permissions()

    # pet adopt korar jonno---------->
    def perform_create(self, serializer):
        user = self.request.user
        
        pet = serializer.validated_data['pet']
        pet_price = pet.price

        print(pet_price)
        print(pet.available)
        print(user.profile.balance)

        if pet.added_by== user:
            raise ValidationError({'error':'You cannot adopt your own pet.'})

        if user.profile.balance < pet_price:
            raise ValidationError({'error':'Insufficient balance to adopt this pet'})
        
        if not pet.available:
            raise ValidationError({'error':'Sorry.! pet is not available'})

        user.profile.balance -= pet_price
        user.profile.save()
        
        pet.available = False
        pet.save()

        adoption = serializer.save(user=user)
        return Response({'message':'Pet adopt successful'},status=status.HTTP_201_CREATED)

# Addoption view er kaj shesh--------------->


# User er sob gula adopt kora pet filter kore ber korchi.......
class AdoptionApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    def get(self,request,user_id=None):
        if user_id is not None:
            adoption = models.AdoptionModel.objects.filter(user__id=user_id)      
        else:
            adoption = models.AdoptionModel.objects.all()
        serializer = serializers.AdoptionSerializer(adoption,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

   
    
# Review  view er kaj start....
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    authentication_classes = [SessionAuthentication,TokenAuthentication]

    def perform_create(self, serializer):
        user = self.request.user
        print('Review user *********** : ',user)
        pet = serializer.validated_data['pet']

        # Check if the user has adopted this pet
        if not models.AdoptionModel.objects.filter(user=user, pet=pet).exists():
            raise ValidationError("You can only review a pet that you have adopted.")

        # Save the review if the pet has been adopted by the user
        serializer.save(reviewer=user)

    # ai action ta use kore pet_id diye protita pet er review ber korbo...
    @action(detail=False, methods=['get'], url_path='pet_id/(?P<pet_id>[^/.]+)')
    def pet_reviews(self, request, pet_id=None):
        # Filter reviews by pet_id
        reviews = models.Review.objects.filter(pet_id=pet_id)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)

# Review view er kaj end.....

