from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
import uuid
from common.models import BaseModel


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)  # Set is_active to True for superusers

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_number = models.CharField(unique=True, max_length=15, blank=True, null=True)
    # phone_number = models.CharField(max_length=20,unique=True)
    email_verified = models.BooleanField(default=False)
    phone_number_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    has_kyc = models.BooleanField(default=False)
    two_factor_enabled = models.BooleanField(default=False)
    two_factor_type = models.CharField(max_length=20,default="email", choices=(("email", "Email"), ("phone_number", "Phone Number")))     
    available_balance = models.DecimalField(('available balance'), max_digits=20, decimal_places=5, default=0.0)
    user_number = models.BigIntegerField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=20, default=None, null=True, blank=True)
    

    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
    
@receiver(pre_save, sender=CustomUser)
def set_user_number(sender, instance, *args, **kwargs):
    if not instance.user_number:
        last_user = sender.objects.order_by('-user_number').first()
        if last_user and last_user.user_number is not None:
            instance.user_number = last_user.user_number + 1
        else:
            instance.user_number = 1

class Pin(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    pin = models.TextField()

    def __str__(self) -> str:
        return str(self.user)