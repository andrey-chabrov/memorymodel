# -*- coding:utf-8 -*-

import os
from datetime import date

from django.test import TestCase

from memorymodel import models
from memorymodel.generator import ModelFromYaml


class ModelFromYamlTest(TestCase):

    def setUp(self):

        self.path = os.path.join(os.path.dirname(__file__), 'test_models.yaml')
        self.app_label = 'memorymodel'

        self.names = ('UsersTest', 'RoomsTest',)
        for name in self.names:
            if hasattr(models, name):
                delattr(models, name)

        ModelFromYaml()(self.path, self.app_label)

    def test_models_created(self):
        for name in self.names:
            self.assertIsNotNone(getattr(models, name, None))

    def test_models(self):

        get_vname = lambda o, n: o._meta.get_field_by_name(n)[0].verbose_name

        obj = models.UsersTest(
            name='test', paycheck=100, date_joined=date(2005, 1, 25))
        for type_, val in ((str, obj.name), (int, obj.paycheck), 
                (date, obj.date_joined)):
            self.assertIsInstance(val, type_)
        for name, val in (
                (u'Имя', get_vname(obj, 'name')), 
                (u'Зарплата', get_vname(obj, 'paycheck')), 
                (u'Дата поступления на работу', get_vname(obj, 'date_joined'))):
            self.assertEquals(val, name)

        obj = models.RoomsTest(department='test', spots=10)
        for type_, val in ((str, obj.department), (int, obj.spots)):
            self.assertIsInstance(val, type_)
        for name, val in (
                (u'Отдел', get_vname(obj, 'department')),
                (u'Вместимость', get_vname(obj, 'spots')),):
            self.assertEquals(val, name)

    def test_wrong_field_type(self):
        field_desc = [{'id': 'test', 'title': 'test', 'type': 'wrong'}]
        self.assertRaises(AssertionError, ModelFromYaml.create_fields, field_desc)

    def test_model_title(self):
        self.assertEquals(models.UsersTest._meta.verbose_name, u'Пользователи')
        self.assertEquals(models.RoomsTest._meta.verbose_name, u'Комнаты')

    def test_app_label(self):
        self.assertEquals(models.UsersTest._meta.app_label, 'memorymodel')
        self.assertEquals(models.RoomsTest._meta.app_label, 'memorymodel')

    def test_app_label_import_error(self):
        app_label = 'wrong'
        self.assertRaises(ImportError, ModelFromYaml(), self.path, app_label)

    def test_module(self):
        self.assertEquals(getattr(models.UsersTest, '__module__', None), 
            'memorymodel.models')
        self.assertEquals(getattr(models.RoomsTest, '__module__', None), 
            'memorymodel.models')

    def test_char_field_length(self):
        self.assertEquals(models.UsersTest._meta.get_field_by_name(
            'name')[0].max_length, 100)
        self.assertEquals(models.RoomsTest._meta.get_field_by_name(
            'department')[0].max_length, 200)
