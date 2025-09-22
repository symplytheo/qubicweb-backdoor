import requests
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404
# from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import User

from .serializers import UserSerializer


import requests
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from .models import User
from .serializers import UserSerializer

class SignupView(generics.CreateAPIView):
    """
    User registration view
    """
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return Response({
                'token': token.key, 
                'user': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    """
    User login view
    """
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {"error": "Username and password required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = get_object_or_404(User, username=username)
        if not user.check_password(password):
            return Response(
                {"error": "Invalid credentials"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(user)
        return Response({
            'token': token.key, 
            'user': serializer.data
        })

class TestTokenView(APIView):
    """
    Test token authentication view
    """
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response("passed!")

class GoogleSignInView(APIView):
    """
    Handle Google Sign-In authentication
    Expects: {'access_token': 'google_access_token'}
    """
    
    def post(self, request):
        access_token = request.data.get('access_token')
        
        if not access_token:
            return Response(
                {'error': 'Access token required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verify token with Google using userinfo endpoint
        google_url = 'https://www.googleapis.com/oauth2/v3/userinfo'
        headers = {'Authorization': f'Bearer {access_token}'}
        
        try:
            response = requests.get(google_url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                return Response({
                    'error': 'Invalid access token',
                    'details': response.json() if response.content else 'No response content'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user_info = response.json()
            email = user_info.get('email')
            
            if not email:
                return Response(
                    {'error': 'Email not provided by Google'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Try to find existing user by email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # Create new user with unique username
                username = email.split('@')[0]
                # Ensure username is unique
                counter = 1
                original_username = username
                while User.objects.filter(username=username).exists():
                    username = f"{original_username}{counter}"
                    counter += 1
                
                user = User.objects.create(
                    username=username,
                    email=email,
                    first_name=user_info.get('given_name', ''),
                    last_name=user_info.get('family_name', ''),
                    is_active=True
                )
                user.set_unusable_password()  # Since they'll use Google auth
                user.save()
            
            # Create or get token
            token, created = Token.objects.get_or_create(user=user)
            serializer = UserSerializer(user)
            
            return Response({
                'token': token.key,
                'user': serializer.data,
                'message': 'Google sign-in successful'
            })
            
        except requests.Timeout:
            return Response(
                {'error': 'Request to Google timed out'}, 
                status=status.HTTP_408_REQUEST_TIMEOUT
            )
        except requests.RequestException as e:
            return Response(
                {'error': f'Network error: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {'error': f'Server error: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



# from rest_framework import generics
# from .models import User
# from .serializers import UserSerializer, LoginSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView


# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class LoginView(TokenObtainPairView):
#     """
#     Custom view to obtain JWT token pair with additional user info.
#     """

#     serializer_class = LoginSerializer