from rest_framework import generics
from .models import User
from .serializers import UserSerializer, LoginSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginView(TokenObtainPairView):
    """
    Custom view to obtain JWT token pair with additional user info.
    """

    serializer_class = LoginSerializer
