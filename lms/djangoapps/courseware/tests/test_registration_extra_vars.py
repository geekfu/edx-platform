# -*- coding: utf-8
"""
Tests for extra registration variables
"""
import json
from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse
from mock import patch


class TestExtraRegistrationVariables(TestCase):
    """
    Test that extra registration variables are properly checked according to settings
    """
    def setUp(self):
        super(TestExtraRegistrationVariables, self).setUp()
        self.url = reverse('create_account')

        self.url_params = {
            'username': 'username',
            'name': 'name',
            'email': 'foo_bar@bar.com',
            'password': 'password',
            'terms_of_service': 'true',
            'honor_code': 'true',
        }

    def test_default_missing_honor(self):
        """
        By default, the honor code must be required
        """
        self.url_params['honor_code'] = ''
        response = self.client.post(self.url, self.url_params)
        self.assertEqual(response.status_code, 400)
        obj = json.loads(response.content)
        self.assertEqual(
            obj['value'],
            u'To enroll, you must follow the honor code.',
        )

    @patch.dict(settings.REGISTRATION_EXTRA_FIELDS, {'honor_code': 'optional'})
    def test_optional_honor(self):
        """
        With the honor code is made optional, should pass without extra vars
        """
        self.url_params['honor_code'] = ''
        response = self.client.post(self.url, self.url_params)
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        self.assertEqual(obj['success'], True)

    @patch.dict(settings.REGISTRATION_EXTRA_FIELDS, {
        'level_of_education': 'hidden',
        'gender': 'hidden',
        'year_of_birth': 'hidden',
        'mailing_address': 'hidden',
        'goals': 'hidden',
        'honor_code': 'hidden',
        'city': 'hidden',
        'country': 'hidden'})
    def test_all_hidden(self):
        """
        When the fields are all hidden, should pass without extra vars
        """
        response = self.client.post(self.url, self.url_params)
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        self.assertTrue(obj['success'])

    @patch.dict(settings.REGISTRATION_EXTRA_FIELDS, {'city': 'required'})
    def test_required_city_missing(self):
        """
        Should require the city if configured as 'required' but missing
        """
        self.url_params['city'] = ''
        response = self.client.post(self.url, self.url_params)
        self.assertEqual(response.status_code, 400)
        obj = json.loads(response.content)
        self.assertEqual(
            obj['value'],
            u'A city is required',
        )

    @patch.dict(settings.REGISTRATION_EXTRA_FIELDS, {'city': 'required'})
    def test_required_city(self):
        """
        Should require the city if configured as 'required' but missing
        """
        self.url_params['city'] = 'New York'
        response = self.client.post(self.url, self.url_params)
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        self.assertTrue(obj['success'])

    @patch.dict(settings.REGISTRATION_EXTRA_FIELDS, {'country': 'required'})
    def test_required_country_missing(self):
        """
        Should require the country if configured as 'required' but missing
        """
        self.url_params['country'] = ''
        response = self.client.post(self.url, self.url_params)
        self.assertEqual(response.status_code, 400)
        obj = json.loads(response.content)
        self.assertEqual(
            obj['value'],
            u'A country is required',
        )

    @patch.dict(settings.REGISTRATION_EXTRA_FIELDS, {'country': 'required'})
    def test_required_country(self):
        self.url_params['country'] = 'New York'
        response = self.client.post(self.url, self.url_params)
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        self.assertTrue(obj['success'])

    @patch.dict(settings.REGISTRATION_EXTRA_FIELDS, {'level_of_education': 'required'})
    def test_required_level_of_education_missing(self):
        """
        Should require the level_of_education if configured as 'required' but missing
        """
        self.url_params['level_of_education'] = ''
        response = self.client.post(self.url, self.url_params)
        self.assertEqual(response.status_code, 400)
        obj = json.loads(response.content)
        self.assertEqual(
            obj['value'],
            u'A level of education is required',
        )

    @patch.dict(settings.REGISTRATION_EXTRA_FIELDS, {'level_of_education': 'required'})
    def test_required_level_of_education(self):
        self.url_params['level_of_education'] = 'p'
        response = self.client.post(self.url, self.url_params)
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        self.assertTrue(obj['success'])

    @patch.dict(settings.REGISTRATION_EXTRA_FIELDS, {'gender': 'required'})
    def test_required_gender_missing(self):
        """
        Should require the gender if configured as 'required' but missing
        """
        self.url_params['gender'] = ''
        response = self.client.post(self.url, self.url_params)
        self.assertEqual(response.status_code, 400)
        obj = json.loads(response.content)
        self.assertEqual(
            obj['value'],
            u'Your gender is required',
        )

    @patch.dict(settings.REGISTRATION_EXTRA_FIELDS, {'gender': 'required'})
    def test_required_gender(self):
        self.url_params['gender'] = 'm'
        response = self.client.post(self.url, self.url_params)
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        self.assertTrue(obj['success'])

    @patch.dict(settings.REGISTRATION_EXTRA_FIELDS, {'year_of_birth': 'required'})
    def test_required_year_of_birth_missing(self):
        """
        Should require the year_of_birth if configured as 'required' but missing
        """
        self.url_params['year_of_birth'] = ''
        response = self.client.post(self.url, self.url_params)
        self.assertEqual(response.status_code, 400)
        obj = json.loads(response.content)
        self.assertEqual(
            obj['value'],
            u'Your year of birth is required',
        )

    @patch.dict(settings.REGISTRATION_EXTRA_FIELDS, {'year_of_birth': 'required'})
    def test_required_year_of_birth(self):
        self.url_params['year_of_birth'] = '1982'
        response = self.client.post(self.url, self.url_params)
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        self.assertTrue(obj['success'])

    @patch.dict(settings.REGISTRATION_EXTRA_FIELDS, {'mailing_address': 'required'})
    def test_required_mailing_address_missing(self):
        """
        Should require the mailing_address if configured as 'required' but missing
        """
        self.url_params['mailing_address'] = ''
        response = self.client.post(self.url, self.url_params)
        self.assertEqual(response.status_code, 400)
        obj = json.loads(response.content)
        self.assertEqual(
            obj['value'],
            u'Your mailing address is required',
        )

    @patch.dict(settings.REGISTRATION_EXTRA_FIELDS, {'mailing_address': 'required'})
    def test_required_mailing_address(self):
        self.url_params['mailing_address'] = 'my address'
        response = self.client.post(self.url, self.url_params)
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        self.assertTrue(obj['success'])

    @patch.dict(settings.REGISTRATION_EXTRA_FIELDS, {'goals': 'required'})
    def test_required_goals_missing(self):
        """
        Should require the goals if configured as 'required' but missing
        """
        self.url_params['goals'] = ''
        response = self.client.post(self.url, self.url_params)
        self.assertEqual(response.status_code, 400)
        obj = json.loads(response.content)
        self.assertEqual(
            obj['value'],
            u'A description of your goals is required',
        )

    @patch.dict(settings.REGISTRATION_EXTRA_FIELDS, {'goals': 'required'})
    def test_required_goals(self):
        self.url_params['goals'] = 'my goals'
        response = self.client.post(self.url, self.url_params)
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.content)
        self.assertTrue(obj['success'])
