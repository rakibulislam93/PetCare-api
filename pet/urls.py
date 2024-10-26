from rest_framework.routers import DefaultRouter
from django.urls import path,include
from . import views

router = DefaultRouter()

router.register('list',views.PetViewSet)

router.register('category',views.CategoryViewSet)
router.register('adoption',views.AdoptionViewSet)
router.register('reviews', views.ReviewViewSet)

urlpatterns = [
    path('',include(router.urls)),
    
    path('user_added/',views.UserAddedPet.as_view(),name='user_added_pet'),
    path('adoption/user/<int:user_id>/',views.AdoptionApiView.as_view(), name='user_adoption'),
]
