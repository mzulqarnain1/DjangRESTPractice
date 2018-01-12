import unittest
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

import django
django.setup()

from django.contrib.auth.models import User


class TestGETPropertyView(TestCase):
    """

    """
    def setUp(self):
        """

        :return:
        """
        self.user = User.objects.create_user(
            username='testuser', password='12345arbi')
        self.client = APIClient()
        self.client._login(user=self.user)

    def test_view(self):
        """

        :return:
        """
        response = self.client.get('/api/property/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestGETPropertyViewWithoutLogin(TestCase):
    """

    """
    def setUp(self):
        self.client = APIClient()

    def test_view(self):
        """

        :return:
        """
        response = self.client.get('/api/property/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


if __name__ == '__main__':
    unittest.main()
