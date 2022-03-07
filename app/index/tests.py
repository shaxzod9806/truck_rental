# Make all requests in the context of a logged in session.
from rest_framework.test import APIClient


def login_user(client):
    """
    Login a user.
    """
    url = 'http://localhost:8000/api/index/login/'
    data = {
        'username': '+998931209806',
        'password': 'string'
    }
    response = client.post(url, data, format='json')
    token = response.data['token']
    client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
    assert response.status_code == 200
    return client


# client = APIClient()
# client.login(username='+998931209806', password='string')

import unittest
from django.test import Client


class testCountry(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details(self):
        # Issue a GET request.
        response = self.client.get('http://localhost:8000/api/customer/country')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)


import json
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from index.models import User
from renter.serializers import UserSerializer


class RegisterTestCase(APITestCase):
    def setUp(self):
        data = {
            "first_name": "string",
            "username": "testcase",
            "password": "string",
            "user_type": 4,
            "device_id": "string"
        }
        response = self.client.post("http://localhost:8000/api/index/register/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
class ProfileTestCase(APITestCase):
    url = 'http://localhost:8000/api/index/login/'
    def setUp(self):
        self.user = User.objects.create_user(username='testcase', password='string')
