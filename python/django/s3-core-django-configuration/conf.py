"""
This file contains everything needed to configure for S3 Storage for core django

More Info: https://blog.theodo.com/2019/07/aws-s3-upload-django/
"""

# ------------------  Installation
"""
pip3 install boto boto3 django-storages
"""

# -------------------- settings.py

# Config here from decouple
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = 'us-east-1'
AWS_S3_ENDPOINT_URL = 'https://s3.us-east-1.amazonaws.com'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"