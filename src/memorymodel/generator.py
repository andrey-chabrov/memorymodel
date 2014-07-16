# -*- coding: utf-8 -*-

import yaml

from django.db import models


class ModelFromYaml(object):

    """
    This is the main class to handle the yaml models.

    "create_model" - the main method that create model classes and add them
    to the "app_label.models" module. 
    """

    @classmethod
    def __call__(cls, path, app_label):
        cls.create_model(path, app_label)

    @staticmethod
    def load_yaml(path):
        return yaml.load(open(path))

    @staticmethod
    def create_fields(fields_description):

        """
        Creates the fields list from the fields description.

        In order to add a new type of field one should add appropriate
        class in "field_types" and rules to treat field description if 
        necessary.
        """

        field_types = {
            'char': models.CharField, 
            'int': models.IntegerField, 
            'date': models.DateField,
        }
        default_lenght = 200

        fields = {'id': models.AutoField(primary_key=True, editable=False,)}
        for fd in fields_description:

            assert fd['type'] in field_types.keys(),\
                'Wrong type of field "%s".' % fd['type']

            other_kwargs = {'max_length': fd.get('length', default_lenght)}\
                if fd['type'] == 'char' else {}
            fields.update({
                fd['id']: field_types[fd['type']](
                    verbose_name=fd['title'],
                    **other_kwargs
                )
            })

        return fields

    @classmethod
    def create_model(cls, path, app_label):

        """
        Create model class and save it to the "app_label.models" module.
        """

        module_name = ''.join((app_label, '.models'))
        app_models = __import__(module_name, fromlist=['models'])
        structure = cls.load_yaml(path)

        for model, fields_str in structure.iteritems():

            attrs = {}
            fields = cls.create_fields(fields_str['fields'])
            attrs.update(fields)
            attrs.update({
                'Meta': type('Meta', (), {
                    'app_label': app_label,
                    'verbose_name': fields_str['title'],
                }),
                '__module__': module_name,
            })

            TempModel = type(model, (models.Model,), attrs)
            setattr(app_models, model, TempModel)
