# Make all requests in the context of a logged in session.
from rest_framework.test import APIClient

import unittest
from django.test import Client


import json
# from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from index.models import User
from renter.serializers import UserSerializer


class RegisterTestCase(APITestCase):
    def test_register(self):
        print('(((((((((((((((((  RegisterTestCase   )))))))))))))))))))')
        data = {
            "first_name": "string",
            "last_name": "string",
            "username": "testcase",
            "password": "1122334455",
            "user_type": 4,
            "device_id": "string"
        }
        response = self.client.post("http://localhost:8000/api/index/register/", data)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testcase')
        self.assertEqual(response.data['first_name'], 'string')
        self.assertEqual(response.data['last_name'], 'string')
        self.assertEqual(response.data['user_type'], 4)
        self.assertEqual(response.data['device_id'], 'string')
        self.assertEqual(data['password'], '1122334455')
        # self.assertEqual(response.data['id'], )
        self.assertEqual(response.data['is_active'], False)

    def test_login_user(self):
        """
        Login a user.
        """
        print('(((((((((((((((((  Login a user.   )))))))))))))))))))')
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()

        c = Client()
        logged_in = c.login(username='testuser', password='12345')
        print(logged_in)


from django.contrib.auth import get_user_model


class ProfileTestCase(APITestCase):
    url = 'http://localhost:8000/api/index/login/'

    def setUp(self):
        print('(((((((((((((((((  ProfileTestCase   )))))))))))))))))))')
        self.user = User.objects.create_user(username='testcase', password='string')
