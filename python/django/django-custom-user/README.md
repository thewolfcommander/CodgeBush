# Django Create Custom User

In this module I've created a custom user integration.

## Configuration

```python

from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.core.validators import EmailValidator


class CustomUserManager(BaseUserManager):
    """
    This manager is for handling user authentication model and functioning
    """
    def create_user(self, email, first_name, last_name, password, **extra_fields):
        """
        This function will create the normal user. It will act as a helper function for creating super users.
        """
        user = self.model(first_name=first_name, email=email, last_name=last_name, *extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        """
        This function will create super user
        """
        user = self.create_user(email, first_name, last_name, password, **extra_fields)
        user.is_admin=True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email):
        """
        This function will set the username of the user to the mobile number
        """
        return self.get(email=email)


class User(PermissionsMixin, AbstractBaseUser):
    """
    Custom user for authentication purpose
    """
    AUTHENTICATION_CHOICES = [
        ('google', 'google'),
        ('normal', 'normal')
    ]
    first_name = models.CharField(max_length=50, null=True, blank=True, help_text="First name for user")
    last_name = models.CharField(max_length=50, null=True, blank=True, help_text="Last name for user")
    email = models.EmailField(
        max_length=255,
        validators=[EmailValidator,],
        help_text="This will be the user's primary email",
        null=True,
        blank=True,
    )
    authentication_method = models.CharField(max_length=50, null=True, blank=True, help_text="Authentication method for registration", choices=AUTHENTICATION_CHOICES)
    is_email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False, help_text="This will determine is the user is a super user or not")

    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    # This object will connect this model to its manager
    objects = CustomUserManager()

    # Setting up the default username field of the user model
    USERNAME_FIELD = 'first_name'

    # Setting up the unique together fields for the user model
    UNIQUE_TOGETHER = ['first_name', 'email']

    # Setting up the required fields for the user model
    REQUIRED_FIELDS = ['email', 'last_name']

    def __str__(self):
        """
        This function is for better representation purposes of the model refernces
        """
        return "{}-{}".format(str(self.id), str(self.email))

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


"""
In Settings.py
"""

AUTH_USER_MODEL = 'accounts.User'


```
