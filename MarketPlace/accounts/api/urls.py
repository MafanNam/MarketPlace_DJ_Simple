"""
URL mappings for the user API.
"""
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

from . import views

app_name = 'accounts'

urlpatterns = [
    # Auth
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist/', TokenBlacklistView.as_view(),
         name='token_blacklist'),

    # User
    path('user/', views.ManagerUserView.as_view(), name='user'),

    # Verification Email
    path('email-activate/', views.VerifyEmail.as_view(),
         name='email_activate'),

    # Resset Password
    path('password-resset-request/', views.RequestResetPasswordEmail.as_view(),
         name='request_resset_password'),
    path('password-reset/<uidb64>/<token>/',
         views.PasswordTokenCheckAPI.as_view(),
         name='password_reset_confirm'),
    path('password-reset-complete/', views.SetNewPasswordAPIView.as_view(),
         name='password_reset_complete'),

    # Profile
    path('profile/', views.UserProfileView.as_view(), name='profile'),
]
