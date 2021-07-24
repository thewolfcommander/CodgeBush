# Django REST Framework - Google Auth Integration

In this module, I've added how to do google authentication using django-rest-framework.

More info: [Click here](https://gerrysabar.medium.com/implementing-google-login-with-jwt-in-django-for-restful-api-authentication-eaa92e50522d)

## Configuration

```python

"""
STEP 1:
Installation:

pip install djangorestframework_simplejwt requests
"""

"""
STEP 2:
Setting default Authentication Class
"""

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}


"""
STEP 3:
View
"""

import requests
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


class GoogleView(APIView):
    """
    Google API view for google authentication
    """

    def post(self, request, format=None):
        """
        Method for post request  for google authentication
        """
        payload = {'access_token': request.data.get("token")}  # validate the token
        r = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', params=payload)
        data = json.loads(r.text)

        if 'error' in data:
            content = {'message': 'wrong google token / this google token is already expired.'}
            return Response(content)

        # create user if not exist
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            user = User()
            user.username = data['email']
            # provider random default password
            user.password = make_password(BaseUserManager().make_random_password())
            user.email = data['email']
            user.save()

        token = RefreshToken.for_user(user)  # generate token without username & password
        response = {}
        response['username'] = user.username
        response['access_token'] = str(token.access_token)
        response['refresh_token'] = str(token)
        return Response(response)
```
