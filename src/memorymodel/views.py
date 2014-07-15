# -*- coding: utf-8 -*-

from annoying import decorators

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory
from django.forms.widgets import DateInput
from django.forms.widgets import HiddenInput
from django.forms.widgets import NumberInput
from django.forms.widgets import TextInput
from django.http import Http404
from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect
from django.utils.encoding import force_text

import memorymodel


@decorators.render_to('home.html')
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


@decorators.ajax_request
def get_formset_data(request, modelname):

    """
    Get formset's data in json format for selected model.
    """

    if not request.is_ajax():
        raise Http404()

    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    model = modelname and getattr(memorymodel.models, modelname, None)
    if model is None:
        return {'errors': ["Wrong model name."]}

    formset = model and modelformset_factory(model)(request.POST or None)

    formset_data = {}
    formset_data.update({'fields': [f.label for f in formset[0].visible_fields()]})

    data = []
    hidden_data = []
    types = {
        DateInput: 'text',
        HiddenInput: 'hidden',
        NumberInput: 'number',
        TextInput: 'text',
    }
    for form in [f for f in formset] + [formset.management_form]:
        form_data = []
        for field in form:
            input = {
                'id': field.id_for_label,
                'type': types[type(field.field.widget)],
                'name': field.html_name,
            }
            value = force_text(field.field.widget._format_value(field.value()))
            if value != 'None':
                input.update({'value': value})
            if type(field.field.widget) is TextInput:
                input.update({'maxlength': str(field.field.max_length)})
            if field.is_hidden:
                hidden_data.append(input)
            else:
                form_data.append(input)
        if form_data:
            data.append(form_data)

    formset_data.update({'data': data})
    formset_data.update({'hidden': hidden_data})

    return formset_data
