# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

import memorymodel


for model_name in ContentType.objects.filter(
        app_label='memorymodel').values_list('model', flat=True):

    model = getattr(memorymodel.models, model_name, None)
    assert model is not None, u'No model named %s.' % model_name

    admin.site.register(model)
