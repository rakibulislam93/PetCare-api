
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# router.register('deposite',views.DepositeViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('register/',views.UserRegistrationApiView.as_view(),name='register'),
    path('activate/<uid64>/<token>',views.activate,name='activate'),
    path('login/',views.UserLoginApiView.as_view(),name='login'),
    path('logout/',views.UserLogoutView.as_view(),name='logout'),
    path('change_password/', views.ChangePassword.as_view(), name='change_password'),
    
    path('update/<int:pk>/',views.ProfileUpdateView.as_view()),
    path('profile/',views.ProfileApiView.as_view(),name='profile_detail'),
    path('deposite/',views.DepositeApiView.as_view(),name='deposite'),
    path('contact/',views.ContactApiView.as_view(),name='contact'),
      
]


