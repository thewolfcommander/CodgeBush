# CodgeBush

CodgeBush is my personal library for hand-picked code snippets to get the work done in plenty of minutes

## How I write configuration snippets

Basically I follow a format to write my handy snippets so that I can find them easily when I need them. So, the steps and format I follow is mentioned below:

- Create a separate folder in appropriate category
  - For Example: django-rest-swagger configuration is created inside directory /python/django/django-rest-swagger/
- After that create a conf.py file inside that folder in which we can mention every configuration that we need for that particular feature step-by-step.
  - For Example: For Django-storages, we first need to install packages then paste settings conf to settings.py
- The next step is to create extra files depending on the feature implementation
  - For Example: For django-storages configuration, and s3 bucket implementation, we need two policies - CORS and BUCKET_POLICY, so I've created the two json files for that.

That's it. We only need to follow these steps to create our handy snippets.
