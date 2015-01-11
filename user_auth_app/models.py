from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.db import models


class UserDetailsValidationException(Exception):
    """
    Exceptions for not proper user's information
    """
    pass


class CustomUserManager(BaseUserManager):

    def create_user(self, username=None, email=None, password=None, **kwargs):

        if not email:
            raise UserDetailsValidationException('Users must have a valid email address. Probably your email doesn\'t confirmed.')

        account = self.model(
            email=self.normalize_email(email), username=username, **kwargs
        )

        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, username, email, password, **kwargs):
        account = self.create_user(username, email, password, **kwargs)

        account.is_superuser = True
        account.save()

        return account


class CustomUser(AbstractBaseUser):

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)

    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    connected_providers = models.CharField(max_length=140, blank=True, default='')

    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['username']

    def __unicode__(self):
        return self.email

    def __str__(self):
        return self.email

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name

