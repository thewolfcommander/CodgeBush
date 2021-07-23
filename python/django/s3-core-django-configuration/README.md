# S3 - Core Django Configuration

This file contains everything needed to configure for S3 Storage for core django. I've used boto3 and django-storages

More Info: [Click here](https://blog.theodo.com/2019/07/aws-s3-upload-django/)

# Configuration

```python


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

```

## CORS Policy

```json
[
  {
    "AllowedHeaders": [],
    "AllowedMethods": ["PUT", "POST", "DELETE", "GET"],
    "AllowedOrigins": ["*"],
    "ExposeHeaders": []
  },
  {
    "AllowedHeaders": [],
    "AllowedMethods": ["PUT", "POST", "DELETE", "GET"],
    "AllowedOrigins": ["http://localhost:8000"],
    "ExposeHeaders": []
  }
]
```

## BUCKET Policy

This policy will allow all objects public - suitable for some use cases

```json
{
  "Version": "2008-10-17",
  "Id": "Policy1397632521960",
  "Statement": [
    {
      "Sid": "Stmt1397633323327",
      "Effect": "Allow",
      "Principal": {
        "AWS": "*"
      },
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::{BUCKET_NAME}/*"
    }
  ]
}
```
