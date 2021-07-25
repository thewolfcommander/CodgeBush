# Django REST Framework file upload - S3 Storage Bucket

In this module, I am going to add snippet for, how to upload file to s3 bucket using django rest framework and boto. This module contains two parts - first is uploading a simple file/image to s3 and second is uploading a base64 image to s3 by converting it to bytearray.

Note: The solution I've implemented is HIT and TRIAL solution and is production ready.

- More Info:
  - [Uplaoding a base64 direct to s3 using botocore.resource](https://newbedev.com/upload-a-base64-string-image-data-to-s3-server-in-python-using-boto3-and-get-url-in-return)
  - [Converting base64 to image](https://gist.github.com/RaminNietzsche/1c270f176e91fc57ecc5bc0468e46aee)
  - [Convert Pillow object to image](https://stackoverflow.com/questions/51725809/convert-pillow-image-object-to-jpegimagefile-object)
  - [Convert PIL object to byte array](https://stackoverflow.com/questions/33101935/convert-pil-image-to-byte-array)

## Installation

```shell

pip install boto boto3 pillow botocore

```

## Uploading simple file to s3 bucket

Note: You need to get AWS_ACCESS_KEY_ID, AWS_ACCESS_SECRET_KEY and bucket name in order to proceed.

```python

"""
File upload handler

You can save it in another file and then import it to your main api views.py to use it as a utility tool
"""

import re
import boto3
import uuid
from datetime import datetime
from botocore.client import Config
from decouple import config as env_config


ACCESS_KEY = env_config('AWS_ACCESS_KEY_ID')
SECRET_KEY = env_config('AWS_SECRET_ACCESS_KEY')
BUCKET_NAME = env_config('S3_BUCKET_NAME')

def get_ext(file):
    m = re.search(r'\.[A-Za-z0-9]+$', file)
    return m.group(0) if m else ""

# print(get_ext("hello.gif"))

def get_file_name(file):
    random_file_name = '-'.join([str(uuid.uuid4().hex[:14]), file])
    return random_file_name

# print(get_file_name("myapp_models.png"))

def upload(file, filetype, name):
    """
    FIle type should be - IMG, VID, DOC, AUD
    """
    data = file
    # print(file)

    s3 = boto3.resource(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        config=Config(signature_version='s3v4')
    )

    REGION='us-east-2'
    today = datetime.now()
    # try:
    file_ext = get_ext(name)

    if file_ext == "":
        file_ext = 'png'
    filename = "NOTEX-{}-{}{}{}{}{}{}{}{}".format(filetype, today.year, today.month, today.day, today.hour, today.minute, today.second, today.microsecond, file_ext)
    filepath = '{}/{}/{}/{}/{}/{}'.format(filetype, today.year, today.month, today.day, today.hour, filename)
    s3.Bucket(BUCKET_NAME).put_object(Key=filepath, Body=data)
    object_acl = s3.ObjectAcl(BUCKET_NAME, filepath)
    response = object_acl.put(ACL='public-read')
    url = 'http://{}.s3.{}.amazonaws.com/{}/{}/{}/{}/{}/{}'.format(str(BUCKET_NAME), str(REGION), str(filetype), str(today.year), str(today.month), str(today.day), str(today.hour), str(filename))

    return url, file_ext


"""
Next create a API view so that you can create an endpoint for the same
"""

from rest_framework.serializers import ValidationError

from rest_framework.parsers import FileUploadParser
from notex.utils import files


class FileUploadView(APIView):
    parser_class = [FileUploadParser]
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        if "file" not in request.data:
            raise ValidationError(detail="FIle should be provided", code=400)
        file_obj = request.data["file"]
        name = request.data['name']   # File name should be given separately, it will be used to get file extension in the utility
        filetype = 'IMG'   # it can be IMG, DOC, VID
        try:
            url, ext = files.upload(file, filetype, name)
        except Exception as e:
            raise ValidationError(detail="Unable to upload file. Reason - {}".format(e), code=400)
        return Response(
            {
                "status": True,
                "message": "File Uploaded",
                "url": url,
            },
            status=201,
        )


"""
After that map the url to view and boom, you are done.
"""

```

## Uploading base64 file data to s3 bucket

Just add the below function to utility and change your api view like below to get things done.

```python

"""
File upload handler

You can save it in another file and then import it to your main api views.py to use it as a utility tool
"""

import base64
from io import BytesIO
from PIL import Image

def image_converter(file):
    """
    This function will convert the base64 to bytearray and then return it to be used by upload handler function.
    """
    starter = file.find(',')
    image_data = file[starter+1:]
    image_data = bytes(image_data, encoding="ascii")
    # im =  Image.open(BytesIO(base64.b64decode(image_data))).convert('RGB')
    im = BytesIO(base64.b64decode(image_data))
    return im

"""
Next create a API view so that you can create an endpoint for the same
"""

from rest_framework.serializers import ValidationError

from rest_framework.parsers import FileUploadParser
from notex.utils import files


class FileUploadView(APIView):
    parser_class = [FileUploadParser]
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        if "file" not in request.data:
            raise ValidationError(detail="FIle should be provided", code=400)
        file_obj = request.data["file"]
        name = request.data['name']
        filetype = 'IMG'
        try:
            byte_array = files.image_converter(file_obj)
            url, ext = files.upload(byte_array, filetype, name)
        except Exception as e:
            raise ValidationError(detail="Unable to upload file. Reason - {}".format(e), code=400)
        return Response(
            {
                "status": True,
                "message": "File Uploaded",
                "url": url,
            },
            status=201,
        )



"""
After that map the url to view and boom, you are done.
"""

```
