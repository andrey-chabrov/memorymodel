# -*- coding: utf-8 -*-

from django.contrib.contenttypes.models import ContentType

from annoying.decorators import render_to

import memorymodel


@render_to('home.html')
def home(request):

    models = ((model._meta.verbose_name, model) for model in
        (getattr(memorymodel.models, model_name) for model_name in 
        ContentType.objects.filter(app_label='memorymodel').values_list(
        'model', flat=True)))

    if request.method == 'POST':
        pass

    return {
        'pagetitle': u'Tables',
        'models': models,
    }
