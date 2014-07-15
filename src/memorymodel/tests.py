# -*- coding:utf-8 -*-

import json
import os

from datetime import date

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

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


class GetFormsetDataViewTest(TestCase):

    fixtures = ['get_formset_data.json']

    def setUp(self):
        self.client = Client()
        self.url = reverse('get_formset_data', kwargs={'modelname': 'users'})

    def test_ajax_request_check(self):
        response = self.client.get(self.url)
        self.assertEqual(404, response.status_code)

    def test_wrong_model_name(self):
        url = reverse('get_formset_data', kwargs={'modelname': 'wrongtest'})
        response = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(
            json.dumps({'errors': ['Wrong model name.']}), 
            response.content
        )

    def test_data(self):
        response = self.client.get(self.url,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(json.dumps({

            'fields': [u'Имя', u'Зарплата', u'Дата поступления на работу'],

            'data': [
            [{
                'id': 'id_form-0-name', 
                'type': 'text', 
                'value': 'test2',
                'name': 'form-0-name',
                'maxlength': '100'
            },
            {
                'id': 'id_form-0-paycheck', 
                'type': 'number', 
                'value': '5',
                'name': 'form-0-paycheck'
            },
            {
                'id': 'id_form-0-date_joined', 
                'type': 'text', 
                'value': '2014-07-10',
                'name': 'form-0-date_joined'
            }],
            [{
                'id': 'id_form-1-name', 
                'type': 'text', 
                'value': 'test1',
                'name': 'form-1-name',
                'maxlength': '100'
            },
            {
                'id': 'id_form-1-paycheck', 
                'type': 'number', 
                'value': '6',
                'name': 'form-1-paycheck'
            },
            {
                'id': 'id_form-1-date_joined', 
                'type': 'text', 
                'value': '2014-07-15',
                'name': 'form-1-date_joined'
            }],
            [{
                'id': 'id_form-2-name', 
                'type': 'text', 
                'name': 'form-2-name',
                'maxlength': '100'
            },
            {
                'id': 'id_form-2-paycheck', 
                'type': 'number', 
                'name': 'form-2-paycheck'
            },
            {
                'id': 'id_form-2-date_joined', 
                'type': 'text', 
                'name': 'form-2-date_joined'
            }]],

            'hidden': [
            {
                'id': 'id_form-0-id', 
                'type': 'hidden', 
                'value': '1',
                'name': 'form-0-id'
            },
            {
                'id': 'id_form-1-id', 
                'type': 'hidden', 
                'value': '2',
                'name': 'form-1-id'
            },
            {
                'id': 'id_form-2-id', 
                'type': 'hidden', 
                'name': 'form-2-id'
            },
            {
                'id': 'id_form-TOTAL_FORMS', 
                'type': 'hidden', 
                'value': '3',
                'name': 'form-TOTAL_FORMS'
            },
            {
                'id': 'id_form-INITIAL_FORMS', 
                'type': 'hidden', 
                'value': '2',
                'name': 'form-INITIAL_FORMS'
            },
            {
                'id': 'id_form-MAX_NUM_FORMS', 
                'type': 'hidden', 
                'value': '1000',
                'name': 'form-MAX_NUM_FORMS'
            }],

            'verbose_name': u'Пользователи',

        }), response.content)

    def test_field_errors(self):
        post = {
            'form-TOTAL_FORMS': '3',
            'form-INITIAL_FORMS': '2',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-paycheck': 'test',
            'form-0-id': '1',
            'form-1-id': '2',
        }
        response = self.client.post(self.url, post,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual({
            'id': 'id_form-0-paycheck', 
            'type': 'number', 
            'value': 'test',
            'name': 'form-0-paycheck',
            'errors': ['Enter a whole number.']
        }, json.loads(response.content)['data'][0][1])

    def test_save(self):
        post = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-paycheck': '4',
            'form-0-id': '',
            'form-0-name': 'test_new',
            'form-0-date_joined': '2014-07-10',
        }
        response = self.client.post(self.url, post,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(1, models.users.objects.filter(name='test_new').count())
