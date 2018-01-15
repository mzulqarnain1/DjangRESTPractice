import unittest

import django
from rest_framework import status
from rest_framework.test import APIClient
from testscenarios import TestWithScenarios

django.setup()

from api import test_constants
from api.models import Property
from django.contrib.auth.models import User


class TestGETPropertyView(TestWithScenarios):
    """
    In this class we will test our property list endpoint with different scenarios
    and assert that we are getting responses according to our expectations.
    """
    scenarios = [
        ('scenario1', {
            'description': """In this scenario , we will login the user hitting our endpoint, so
                              response will be OK.""",
            'end_point': test_constants.PROPERTY_LIST_ENDPOINT,
            'login': True,
            'expected_response': status.HTTP_200_OK}),
        ('scenario2', {
            'description': """In this scenario , we will not login the user before accessing property
                              view, so access will be forbidden and response will be 403.""",
            'end_point': test_constants.PROPERTY_LIST_ENDPOINT,
            'login': False,
            'expected_response': status.HTTP_403_FORBIDDEN}),
        ('scenario3', {
            'description': """In this scenario , we will login and access specific property endpoint
                              and we will get response 200""",
            'end_point': test_constants.PROPERTY_ENDPOINT,
            'login': True,
            'expected_response': status.HTTP_200_OK}),
        ('scenario4', {
            'description': """In this scenario , we will not login the user before accessing property
                              view, so access will be forbidden and response will be 403.""",
            'end_point': test_constants.PROPERTY_ENDPOINT,
            'login': False,
            'expected_response': status.HTTP_403_FORBIDDEN})]

    def __init__(self, *args, **kwargs):
        """
        Initializing different variables to be used in testing
        """
        super(TestGETPropertyView, self).__init__(*args, **kwargs)
        self.login = False
        self.expected_response = None
        self._property = None
        self.end_point = None

    def setUp(self):
        """
        In setup method we will create objects required for testing.
        """
        self.user = User.objects.create_user(
            username='testuser', password='12345arbi')
        self.client = APIClient()

        if self.login:
            self.client._login(user=self.user)

        if self.end_point == test_constants.PROPERTY_ENDPOINT:
            _property = Property(address='Testing Address',
                                 type_id=1, status_id=2,
                                 owner_id=self.user.id)
            _property.save()
            self.end_point = self.end_point.format(_property.id)

    def test_view_get(self):
        """
        In this test we will hit _property list endpoint and assert responses.
        """
        response = self.client.get(self.end_point)

        self.assertEqual(response.status_code, self.expected_response)

    def tearDown(self):
        """
        Deleting objects created for testing purposes.
        """
        if self._property:
            self._property.delete()
        self.user.delete()


class TestPOSTPropertyView(TestWithScenarios):
    """
    In this class we will test our property list endpoint with different scenarios
    and assert that we are getting responses according to our expectations.
    """
    scenarios = [
        ('scenario1', {
            'description': """""",
            'data': {'address': 'Test', 'type': 1, 'status': 2},
            'end_point': test_constants.PROPERTY_LIST_ENDPOINT,
            'login': False,
            'expected_response': status.HTTP_403_FORBIDDEN}),
        ('scenario2', {
            'description': """""",
            'data': {'address': 'Test', 'type': 1, 'status': 2},
            'end_point': test_constants.PROPERTY_LIST_ENDPOINT,
            'login': True,
            'expected_response': status.HTTP_201_CREATED}),
        ('scenario3', {
            'description': """""",
            'data': {'address': 'Test', 'status': 2},
            'end_point': test_constants.PROPERTY_LIST_ENDPOINT,
            'login': True,
            'expected_response': status.HTTP_400_BAD_REQUEST}),
    ]

    def __init__(self, *args, **kwargs):
        """
        Initializing different variables to be used in testing
        """
        super(TestPOSTPropertyView, self).__init__(*args, **kwargs)
        self.login = False
        self.expected_response = None
        self.end_point = None
        self.data = None

    def setUp(self):
        """
        In setup method we will create objects required for testing.
        """
        self.user = User.objects.create_user(
            username='testuser', password='12345arbi')
        self.client = APIClient()

        if self.login:
            self.client._login(user=self.user)

    def test_view_post(self):
        """
        In this test we will hit _property list endpoint and assert responses.
        """
        response = self.client.post(self.end_point, data=self.data)

        self.assertEqual(response.status_code, self.expected_response)

    def tearDown(self):
        """
        Deleting objects created for testing purposes.
        """
        self.user.delete()


if __name__ == '__main__':
    unittest.main()
