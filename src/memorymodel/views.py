# -*- coding: utf-8 -*-

from annoying.decorators import render_to

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory
from django.http import Http404
from django.shortcuts import redirect

import memorymodel


@render_to('home.html')
def home(request, modelname=None):

    models = ((model_name, model._meta.verbose_name, model) for model_name, model in
        ((model_name, getattr(memorymodel.models, model_name)) for model_name in 
        ContentType.objects.filter(app_label='memorymodel').values_list(
        'model', flat=True)))

    model = modelname and getattr(memorymodel.models, modelname, None)
    if modelname is not None and model is None:
        raise Http404()

    formset = model and modelformset_factory(model)(request.POST or None)

    if request.method == 'POST':
        if formset.is_valid():
            formset.save()
            return redirect(reverse('model', kwargs={'modelname': modelname}))

    return {
        'pagetitle': u'Tables',
        'models': models,
        'formset': formset,
        'verbose_name': model and model._meta.verbose_name,
    }
