"""
This file contains the configuration for setting up django-rest-swagger for django-rest-framework to visualize REST APIs with django-rest-framework

FOR more info:

Documentation - https://django-rest-swagger.readthedocs.io/en/latest/#installation

https://stackoverflow.com/questions/55929472/django-templatesyntaxerror-staticfiles-is-not-a-registered-tag-library

https://stackoverflow.com/questions/57654243/how-to-fix-attributeerror-at-api-doc-autoschema-object-has-no-attribute-ge

"""

"""
STEP 1:
Install the packages

pip3 install django-rest-swagger

"""


"""
STEP 2:
Add it to installed apps
"""

INSTALLED_APPS = [
    'rest_framework_swagger',
]



"""
STEP 3:
Make Class Based View or Function based view to customize advanced visualization schema
"""

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger import renderers


class SwaggerSchemaView(APIView):
    """
    Class based View
    """
    permission_classes = [AllowAny]
    renderer_classes = [
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer
    ]

    def get(self, request):
        generator = SchemaGenerator()
        schema = generator.get_schema(request=request)

        return Response(schema)



from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import response, schemas

@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def schema_view(request):
    """
    Function based view
    """
    generator = schemas.SchemaGenerator(title='Pastebin API')
    return response.Response(generator.get_schema(request=request))



"""
STEP 4:

Setup URL to map View - NOTE: For default configuration. But if we have customized advanced configuration then we need to map above views to urlpatterns
"""
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path('', schema_view)
]



"""
Optional - If error comes
"""

# Error 1: Schema related error for django-rest-framework
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}


# Error 2: Staticfiles related error


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            # NOTE: This is main- replace whole templates dictionary if possible
            'libraries' : {
                'staticfiles': 'django.templatetags.static', 
            }
        },
    },
]