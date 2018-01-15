"""
This module contains tests for all of our API endpoints on different scenarios,
of GET, POST, PUT and DELETE.
"""
import mock
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from testscenarios import TestWithScenarios

from api import test_constants
from api.models import Property, PropertyType, Status


class TestGETMethodsOfViews(TestWithScenarios):
    """
    In this class we will test our property list endpoint with different scenarios
    and assert that we are getting responses according to our expectations.
    """
    scenarios = [
        ('scenario1', {
            'description': """In this scenario , we will login the user hitting our property
                              list endpoint, so response will be OK.""",
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
            'expected_response': status.HTTP_403_FORBIDDEN}),
        ('scenario5', {
            'description': """In this scenario , user will be hitting status list endpoint, so response
                              will be OK.""",
            'end_point': test_constants.STATUS_ENDPOINT,
            'login': False,
            'expected_response': status.HTTP_200_OK}),
        ('scenario6', {
            'description': """In this scenario , user will be hitting type list endpoint, so response
                              will be OK.""",
            'end_point': test_constants.TYPE_ENDPOINT,
            'login': False,
            'expected_response': status.HTTP_200_OK}),
        ('scenario7', {
            'description': """In this scenario, user is hitting users list endpoint without login, so
                              request will be forbidden.""",
            'end_point': test_constants.USERS_ENDPOINT,
            'login': False,
            'expected_response': status.HTTP_403_FORBIDDEN}),
        ('scenario8', {
            'description': """In this scenario, user is hitting users list endpoint with login, so
                              request will be Ok.""",
            'end_point': test_constants.USERS_ENDPOINT,
            'login': True,
            'expected_response': status.HTTP_200_OK}),
        ('scenario9', {
            'description': """In this scenario, user is hitting user retrieval endpoint without login, so
                              request will be forbidden.""",
            'end_point': test_constants.USER_ENDPOINT,
            'login': False,
            'expected_response': status.HTTP_403_FORBIDDEN}),
        ('scenario10', {
            'description':  """In this scenario, user is hitting user retrieval endpoint with login, so
                              request will be OK.""",
            'end_point': test_constants.USER_ENDPOINT,
            'login': True,
            'expected_response': status.HTTP_200_OK}),
        ('scenario11', {
            'description': """In this scenario , user will access specific status endpoint
                              and we will get response 200""",
            'end_point': test_constants.STATUS_ENDPOINT_2,
            'login': True,
            'expected_response': status.HTTP_200_OK}),
        ('scenario12', {
            'description': """In this scenario , user will access specific property type endpoint
                              and we will get response 200""",
            'end_point': test_constants.TYPE_ENDPOINT_2,
            'login': True,
            'expected_response': status.HTTP_200_OK})
    ]

    def __init__(self, *args, **kwargs):
        """
        Initializing different variables to be used in testing
        """
        super(TestGETMethodsOfViews, self).__init__(*args, **kwargs)
        self.login = False
        self.expected_response = None
        self._property = None
        self.end_point = None
        self._type = None
        self._status = None

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

        elif self.end_point == test_constants.USER_ENDPOINT:
            self.end_point = self.end_point.format(self.user.id)

        elif self.end_point == test_constants.STATUS_ENDPOINT_2:
            self._status = Status(name='Test')
            self._status.save()
            self.end_point = self.end_point.format(self._status.id)

        elif self.end_point == test_constants.TYPE_ENDPOINT_2:
            self._type = PropertyType(name='Test')
            self._type.save()
            self.end_point = self.end_point.format(self._type.id)

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
        if self._type:
            self._type.delete()
        if self._status:
            self._status.delete()
        self.user.delete()


class TestPOSTPropertyView(TestWithScenarios):
    """
    In this class we will test our property list endpoint with different scenarios
    and assert that we are getting responses according to our expectations.
    """
    scenarios = [
        ('scenario1', {
            'description': """In this scenario, user is not login, so request will
                              be forbidden.""",
            'data': {'address': 'Test', 'type': 1, 'status': 2},
            'end_point': test_constants.PROPERTY_LIST_ENDPOINT,
            'login': False,
            'expected_response': status.HTTP_403_FORBIDDEN}),
        ('scenario2', {
            'description': """In this scenario, user is login and data is complete
                              so a new object will be created.""",
            'data': dict(address='Test'),
            'end_point': test_constants.PROPERTY_LIST_ENDPOINT,
            'login': True,
            'expected_saved': 1,
            'expected_data' : dict(address='Test'),
            'expected_response': status.HTTP_201_CREATED}),
        ('scenario3', {
            'description': """In this scenario, user is login, but required fields are
                              not complete, so response will be bad request.""",
            'data': dict(address='Test'),
            'complete': False,
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
        self.expected_saved = 0
        self.complete = True
        self.expected_data = dict()

    def setUp(self):
        """
        In setup method we will create objects required for testing.
        """
        self.user = User.objects.create_user(
            username='testuser', password='12345arbi')
        self.client = APIClient()

        if self.login:
            self.client._login(user=self.user)

        self.prop_status = Status(name='To Rent')
        self.prop_status.save()
        self.prop_type = PropertyType(name='Flat')
        self.prop_type.save()
        self.expected_data['status'] = self.prop_status.id
        self.expected_data['type'] = self.prop_type.id

        self.data['status'] = self.prop_status.id
        if self.complete:
            self.data['type'] = self.prop_type.id

    def test_view_post(self):
        """
        In this test we will hit _property list endpoint and assert responses.
        """

        response = self.client.post(self.end_point, self.data, format='json')
        self.assertEqual(response.status_code, self.expected_response)

        if self.expected_response == status.HTTP_201_CREATED:
            for attr, value in self.expected_data.items():
                self.assertEqual(response.data[attr], value)

    def tearDown(self):
        """
        Deleting objects created for testing purposes.
        """
        self.prop_type.delete()
        self.prop_status.delete()
        self.user.delete()


class TestPUTPropertyView(TestWithScenarios):
    """
    In this class we will test our property list endpoint with different scenarios
    and assert that we are getting responses according to our expectations.
    """
    scenarios = [
        ('scenario1', {
            'description': """In this scenario, user is not login, so request will
                              be forbidden.""",
            'data': {'address': 'Test-Update', 'type': 1, 'status': 2},
            'end_point': test_constants.PROPERTY_ENDPOINT,
            'login': False,
            'expected_response': status.HTTP_403_FORBIDDEN}),
        ('scenario2', {
            'description': """In this scenario, user is login and data is complete
                              so object will be updated.""",
            'data': {'address': 'Test-Update'},
            'end_point': test_constants.PROPERTY_ENDPOINT,
            'login': True,
            'expected_saved': 1,
            'expected_response': status.HTTP_200_OK,
            'expected_data': dict(address='Test-Update')}),
        ('scenario3', {
            'description': """In this scenario, user is login, but required fields are
                              not complete, so response will be bad request.""",
            'data': {'address': 'Test-Update', 'status': 2},
            'end_point': test_constants.PROPERTY_ENDPOINT,
            'login': True,
            'complete': False,
            'expected_response': status.HTTP_400_BAD_REQUEST}),
    ]

    def __init__(self, *args, **kwargs):
        """
        Initializing different variables to be used in testing
        """
        super(TestPUTPropertyView, self).__init__(*args, **kwargs)
        self.login = False
        self.expected_response = None
        self.end_point = None
        self.data = None
        self.expected_saved = 0
        self.expected_data = dict()
        self.complete = True

    def setUp(self):
        """
        In setup method we will create objects required for testing.
        """
        self.user = User.objects.create_user(
            username='testuser', password='12345arbi')
        self.client = APIClient()

        if self.login:
            self.client._login(user=self.user)
        self.prop_status = Status(name='To Rent')
        self.prop_status.save()
        self.prop_type = PropertyType(name='Flat')
        self.prop_type.save()
        self._property = Property(address='Testing Address',
                                  type_id=self.prop_type.id,
                                  status_id=self.prop_status.id,
                                  owner_id=self.user.id)
        self.expected_data['status'] = self.prop_status.id
        self.expected_data['type'] = self.prop_type.id
        self.data['status'] = self.prop_status.id
        if self.complete:
            self.data['type'] = self.prop_type.id
        self._property.save()
        self.end_point = self.end_point.format(self._property.id)

    def test_view_put(self):
        """
        In this test we will hit _property list endpoint and assert responses.
        """
        response = self.client.put(self.end_point, self.data, format='json')
        self.assertEqual(response.status_code, self.expected_response)

        if self.expected_response == status.HTTP_200_OK:
            for attr, value in self.expected_data.items():
                self.assertEqual(response.data[attr], value)

    def tearDown(self):
        """
        Deleting objects created for testing purposes.
        """
        self.prop_type.delete()
        self.prop_status.delete()
        self.client.logout()
        self._property.delete()
        self.user.delete()


class TestDELETEPropertyView(TestWithScenarios):
    """
    In this class we will test our property list endpoint with different scenarios
    and assert that we are getting responses according to our expectations.
    """
    scenarios = [
        ('scenario1', {
            'description': """In this scenario , we are trying to delete a property
                              without login, so request will be forbidden""",
            'end_point': test_constants.PROPERTY_ENDPOINT,
            'login': False,
            'expected_response': status.HTTP_403_FORBIDDEN}),
        ('scenario2', {
            'description': """In this scenario, we are deleting a property after login
                              and login user is original owner, so property will be
                              deleted.""",
            'end_point': test_constants.PROPERTY_ENDPOINT,
            'login': True,
            'expected_delete': 1,
            'expected_response': status.HTTP_204_NO_CONTENT}),
        ('scenario3', {
            'description': """In this scenario, we are deleting a property after login
                              but login user is not original owner, so request will be
                              forbidden""",
            'end_point': test_constants.PROPERTY_ENDPOINT,
            'login': True,
            'other_user': True,
            'expected_response': status.HTTP_403_FORBIDDEN})]

    def __init__(self, *args, **kwargs):
        """
        Initializing different variables to be used in testing
        """
        super(TestDELETEPropertyView, self).__init__(*args, **kwargs)
        self.login = False
        self.expected_response = None
        self.end_point = None
        self.expected_delete = 0
        self.other_user = None

    def setUp(self):
        """
        In setup method we will create objects required for testing.
        """
        self.user = User.objects.create_user(
            username='testuser', password='12345arbi')

        if self.other_user:
            self.user_2 = User.objects.create_user(
                username='testuser2', password='12345')
        self.client = APIClient()

        if self.login:
            self.client._login(user=self.user)

        if self.other_user:
            user_id = self.user_2.id
        else:
            user_id = self.user.id
        self._property = Property(address='Testing Address',
                                  type_id=1, status_id=2,
                                  owner_id=user_id)
        self._property.save()
        self.end_point = self.end_point.format(self._property.id)

    def test_view_delete(self):
        """
        In this test we will hit _property list endpoint and assert responses.
        """
        with mock.patch.object(Property, 'delete') as delete_prop:
            response = self.client.delete(self.end_point)
        self.assertEqual(response.status_code, self.expected_response)

        self.assertEqual(delete_prop.call_count, self.expected_delete)

    def tearDown(self):
        """
        Deleting objects created for testing purposes.
        """
        self.client.logout()
        self._property.delete()
        if self.other_user:
            self.user_2.delete()
        self.user.delete()


class TestDeleteUpdateUserView(TestWithScenarios):
    """
    In this class we will test our property list endpoint with different scenarios
    and assert that we are getting responses according to our expectations.
    """
    scenarios = [
        ('scenario1', {
            'description': """In this scenario , we are trying to delete a user
                              without login, so request will be forbidden""",
            'end_point': test_constants.USER_ENDPOINT,
            'login': False,
            'expected_response': status.HTTP_403_FORBIDDEN}),
        ('scenario2', {
            'description': """In this scenario, we are deleting a user after login
                              and login user is target user, so user will be
                              deleted.""",
            'end_point': test_constants.USER_ENDPOINT,
            'login': True,
            'expected_delete': 1,
            'expected_response': status.HTTP_204_NO_CONTENT}),
        ('scenario3', {
            'description': """In this scenario, we are deleting a user after login
                              and login user is not target user, so user will not be
                              deleted.""",
            'end_point': test_constants.USER_ENDPOINT,
            'login': True,
            'other_user': True,
            'expected_response': status.HTTP_403_FORBIDDEN})]

    def __init__(self, *args, **kwargs):
        """
        Initializing different variables to be used in testing
        """
        super(TestDeleteUpdateUserView, self).__init__(*args, **kwargs)
        self.login = False
        self.expected_response = None
        self.end_point = None
        self.expected_delete = 0
        self.other_user = None

    def setUp(self):
        """
        In setup method we will create objects required for testing.
        """
        self.user = User.objects.create_user(
            username='testuser', password='12345arbi')

        if self.other_user:
            self.user_2 = User.objects.create_user(
                username='testuser2', password='12345')
        self.client = APIClient()

        if self.login:
            self.client._login(user=self.user)

        if self.other_user:
            user_id = self.user_2.id
        else:
            user_id = self.user.id

        self.end_point = self.end_point.format(user_id)

    def test_view_delete(self):
        """
        In this test we will hit _property list endpoint and assert responses.
        """
        with mock.patch.object(User, 'delete') as delete_prop:
            response = self.client.delete(self.end_point)
        self.assertEqual(response.status_code, self.expected_response)

        self.assertEqual(delete_prop.call_count, self.expected_delete)

    def tearDown(self):
        """
        Deleting objects created for testing purposes.
        """
        self.client.logout()
        if self.other_user:
            self.user_2.delete()
        self.user.delete()

