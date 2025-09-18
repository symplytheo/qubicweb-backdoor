from django.shortcuts import render
from rest_framework import generics
from .models import CustomUser
from .serializers import UserSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class LoginView(TokenObtainPairView):
    """
    Custom view to obtain JWT token pair with additional user info.
    """

    serializer_class = CustomTokenObtainPairSerializer
