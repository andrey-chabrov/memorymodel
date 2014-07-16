# -*- coding: utf-8 -*-

from annoying import decorators

from django.contrib.contenttypes.models import ContentType
from django.forms.models import modelformset_factory
from django.forms.widgets import DateInput
from django.forms.widgets import HiddenInput
from django.forms.widgets import NumberInput
from django.forms.widgets import TextInput
from django.http import Http404
from django.shortcuts import redirect
from django.utils.encoding import force_text

import memorymodel


@decorators.render_to('home.html')
def home(request):

    models = (
        (model_name, getattr(memorymodel.models, model_name)._meta.verbose_name) 
        for model_name in ContentType.objects.filter(
            app_label='memorymodel').values_list('model', flat=True))

    return {
        'pagetitle': u'Tables',
        'models': models,
    }


@decorators.ajax_request
def edit(request, modelname):

    """
    Ajax view for editing selected model.
    """

    if not request.is_ajax():
        raise Http404()

    model = modelname and getattr(memorymodel.models, modelname, None)
    if model is None:
        return {'errors': ["Wrong model name."]}

    formset = model and modelformset_factory(model)(request.POST or None)

    if request.method == 'POST':
        if formset.is_valid():
            formset.save()
            return redirect(request.path)

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
                visible_field = {'attrs': input}
                if request.method == 'POST' and field.errors:
                    visible_field.update({'errors': field.errors})
                form_data.append(visible_field)
        if form_data:
            data.append(form_data)

    formset_data.update({'data': data})
    formset_data.update({'hidden': hidden_data})
    formset_data.update({'verbose_name': model._meta.verbose_name})
    formset_data.update({'action': request.path})

    return formset_data
