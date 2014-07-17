"""
WSGI config for memorymodel project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

import memorymodel
from memorymodel.generator import ModelFromYaml

# Use this path and app_label for example.
path = os.path.join(os.path.dirname(memorymodel.generator.__file__), 'models.yaml')
app_label = 'memorymodel'
ModelFromYaml()(path, app_label)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
