"""
Create models for User
"""
import os
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    """UserManager for Users."""

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("username", email.split('@')[0])

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """User model"""

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50, blank=True)

    # additional fields
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(_('active'), default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name.title()} {self.last_name.title()}"

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


def get_upload_path_profile(instance, filename):
    return os.path.join(
        "UserProfile", "user_%d" % instance.user.id,
        "profile_images", filename)


class UserProfile(models.Model):
    """UserProfile model"""
    user = models.OneToOneField(
        'User', on_delete=models.CASCADE, blank=True, null=True,
        related_name='user_profile')
    profile_image = models.ImageField(
        upload_to=get_upload_path_profile,
        default='static/images/default/default_profile.png')
    telebotId = models.CharField(max_length=255, null=True, blank=True)

    # additional fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

    def get_full_name(self):
        return f"{self.user.first_name.title()} {self.user.last_name.title()}"
