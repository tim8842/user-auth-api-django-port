from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from __future__ import annotations

class UserManager(BaseUserManager):
    def create_user(self, email: str, password=None, **extra_fields) -> User:
        if not email:
            raise ValueError('The email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password=None, **extra_fields) -> User:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)
    
    
# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)    
    is_active = models.BooleanField(default=True)
    is_staff  = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    def __str__(self) -> str:
        return self.email