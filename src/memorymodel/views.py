# -*- coding: utf-8 -*-

from django.contrib.contenttypes.models import ContentType
from django.forms.models import modelformset_factory

from annoying.decorators import render_to

import memorymodel


@render_to('home.html')
def home(request, modelname=None):

    models = ((model_name, model._meta.verbose_name, model) for model_name, model in
        ((model_name, getattr(memorymodel.models, model_name)) for model_name in 
        ContentType.objects.filter(app_label='memorymodel').values_list(
        'model', flat=True)))

    model = modelname and getattr(memorymodel.models, modelname, None)
    formset = model and modelformset_factory(model)()

    if request.method == 'POST':
        pass

    return {
        'pagetitle': u'Tables',
        'models': models,
        'formset': formset,
        'verbose_name': model and model._meta.verbose_name,
    }
