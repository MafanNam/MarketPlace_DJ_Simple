"""
URL mappings for the social_auth API.
"""
from django.urls import path

from social_auth.api import views

from . import views

app_name = 'social_auth'

urlpatterns = [
    # Google auth
    path('google/', views.GoogleSocialAuthView.as_view(), name='google_auth'),
]
