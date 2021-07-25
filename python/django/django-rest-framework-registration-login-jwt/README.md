# Django REST Framework - User Registration Login - JWT authentication

This module deals with the registration and login feature of user using django rest framework and JWT Authentication. No extra configuration needed, just a package needed to manage authentication tokens.

#### Dependency

This module is dependent on Custom user Model. If you want to implement custom user model, then you can [click here](python/django/django-custom-user/README.md)

## Configuation and Snippet

```python

"""
Step 1:
Install package

pip install djangorestframework_simplejwt
"""

"""
Step 2:
Set Default Authentication Class in Settings.py
"""

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

"""
Step 3:
Making serializers
"""

from rest_framework import serializers
from .models import User


class ObtainTokenSerializer(serializers.Serializer):
    """
    Serializer for Logging in
    """
    email = serializers.EmailField()
    password = serializers.CharField(max_length=20)

    def validate(self, attrs):
        """
        Validating the fields - email and password
        """
        email = attrs.get('email')
        password = attrs.get('password')
        # Getting the user object from the database
        user_obj = User.objects.filter(email=email, is_active=True).first()

        # check if the user exists
        if user_obj is None:
            raise serializers.ValidationError("No user exists with this Email")

        # Check if password matches
        if not user_obj.check_password(password):
            raise serializers.ValidationError("Password entered is incorrect")

        return attrs



class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new user
    """
    class Meta:
        model = User
        fields = [
            'password',
            'first_name',
            'last_name',
            'profile_img',
            'email',
            'authentication_method',
            'is_email_verified',
            'is_active',
            'created_timestamp',
            'updated_timestamp'
        ]

    def validate(self, attrs):
        """
        Validating fields for any mistake in input
        """

        email = attrs.get('email')
        password = attrs.get('password')
        if not email:
            raise serializers.ValidationError("You should enter your email address")

        user_obj = User.objects.filter(email=email, is_active=True).first()

        if user_obj is not None:
            if not user_obj.is_email_verified:
                raise serializers.ValidationError("You have registered but your email is not verified. Kindly Proceed to Login and verify your email address.")
            raise serializers.ValidationError("A user exists with this email")
        return attrs


"""
Step 4:
Making Views
"""
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from . import serializers as acc_serializers
from .models import User


class LoginAPIView(APIView):
    """
    This View will return useful user information after successful login along with access and refresh tokens

    TODO: Implement handling unverified email flow
    """
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        """
        POST method that enables the user to log in
        """
        # Getting serialized Data
        serializer = acc_serializers.ObtainTokenSerializer(data=request.data)
        if serializer.is_valid():
            # If serialized data is valid
            #  Getting the user object for the mobile number input from user
            user_obj = User.objects.get(
                email=serializer.validated_data["email"]
            )
            if user_obj.is_active:
                token = RefreshToken.for_user(user_obj)  # generate token without username amnd password
                return Response(
                    data={
                        "status": True,
                        "access_token": str(token.access_token),
                        "refresh_token": str(token),
                        "user": {
                            "id": user_obj.id,
                            "first_name": user_obj.first_name,
                            "last_name": user_obj.last_name,
                            "email": user_obj.email,
                            "profile_img": user_obj.profile_img,
                            "authentication_method": user_obj.authentication_method,
                            "is_active": user_obj.is_active,
                            "is_email_verified": user_obj.is_email_verified,
                            "created_timestamp": user_obj.created_timestamp,
                            "updated_timestamp": user_obj.updated_timestamp
                        },
                        "message": "User logged in Successfully",
                    },
                    status=200
                )
            else:
                raise ValidationError(detail="Invalid User. Unable to Login", code=400)
        elif not serializer.is_valid():
            try:
                raise ValidationError(detail="{}".format(
                            str(serializer.errors["non_field_errors"][0])
                        ), code=400)
            except:
                for i in serializer.errors:
                    raise ValidationError(detail="{}".format(
                                str(serializer.errors[i][0]), str(i)
                            ), code=400)
        else:
            raise ValidationError(detail="Some unknown Error occured. Please try again later.", code=400)


class RegisterAPIView(APIView):
    """
    This register route will return useful user information only along with token

    TODO: Implement Email Verification FLow
    """

    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        """
        method for enabling user to register on Notex APP
        """
        serializer = acc_serializers.UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data["password"]
            user_obj = serializer.save()
            user_obj.authentication_method = 'normal'
            user_obj.is_active = True
            user_obj.profile_img = 'https://images.pexels.com/photos/157675/fashion-men-s-individuality-black-and-white-157675.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260'
            user_obj.set_password(password)
            user_obj.save()
            token = RefreshToken.for_user(user_obj)  # generate token without username amnd password
            return Response(
                data={
                    "status": True,
                    "access_token": str(token.access_token),
                    "refresh_token": str(token),
                    "user": {
                        "id": user_obj.id,
                        "first_name": user_obj.first_name,
                        "last_name": user_obj.last_name,
                        "email": user_obj.email,
                        "profile_img": user_obj.profile_img,
                        "authentication_method": user_obj.authentication_method,
                        "is_active": user_obj.is_active,
                        "is_email_verified": user_obj.is_email_verified,
                        "created_timestamp": user_obj.created_timestamp,
                        "updated_timestamp": user_obj.updated_timestamp
                    },
                    "message": "User logged in Successfully",
                },
                status=201
            )

        elif not serializer.is_valid():
            try:
                raise ValidationError(detail="{}".format(
                            str(serializer.errors["non_field_errors"][0])
                        ), code=400)
            except:
                for i in serializer.errors:
                    raise ValidationError(detail="{} - Error in {}".format(
                                str(serializer.errors[i][0]), str(i)
                            ), code=400)
        else:
            raise ValidationError(detail="Some unknown Error occured. Please try again later.", code=400)

        raise ValidationError(detail=serializer.errors, code=400)


"""
Step 5:
Mapping URLs to Views
"""

urlpatterns = [
    path('auth/login/', views.LoginAPIView.as_view(), name='login'),
    path('auth/register/', views.RegisterAPIView.as_view(), name='register'),
]

```
