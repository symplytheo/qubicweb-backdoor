from django.urls import path
from .views import SignupView, LoginView, TestTokenView, GoogleSignInView

# from . import views

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('test_token/', TestTokenView.as_view(), name='test_token'),
    path('google_signin/', GoogleSignInView.as_view(), name='google_signin')
]


# from django.urls import path
# from .views import RegisterView, LoginView
# from rest_framework_simplejwt.views import TokenRefreshView


# urlpatterns = [
#     path("register/", RegisterView.as_view(), name="register"),
#     path("login/", LoginView.as_view(), name="login"),
#     path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
# ]