# Django Filters Integration with DRF

In this module I've integrated django-filter module with Django REST Framework

- More Info: [Click here](https://django-filter.readthedocs.io/en/stable/guide/rest_framework.html)

## Configuration

```python

"""
STEP 1:
Installation

pip install django-filter
"""

"""
Step 2:
Configuring settings.py
"""

INSTALLED_APPS = [
    ...
    'rest_framework',
    'django_filters',
]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        ...
    ),
}

"""
Step 3:
Using in views
"""

class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('category', 'in_stock')  # This is the shortcut.


```
