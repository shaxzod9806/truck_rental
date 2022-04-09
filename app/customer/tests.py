from django.test import TestCase
from rest_framework.test import APIClient

import unittest
from django.test import Client
from customer.models import Country, Region


# Create your tests here.

class Country_Unit(unittest.TestCase):
    def setUp(self):
        self.client = APIClient()
        self.Country = Country.objects.create(country_name='UZB')
        self.Region = Region.objects.create(region_name='Toshkent', country=self.Country)
        # print(self.Country)
        # print(self.Region)
        # self.client = Client()

    def test_details(self):
        print('(((((((((((((((((  testCountry   )))))))))))))))))))')
        # Issue a GET request.
        response = self.client.get('http://localhost:8000/api/customer/country')
        # print(response.data)
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['country_name'], 'UZB')
        self.assertEqual(response.data[0]['id'], 1)

    def test_region(self):
        print('(((((((((((((((((  testRegion   )))))))))))))))))))')
        # Issue a GET request.
        response = self.client.get('http://localhost:8000/api/customer/region?country_id=1')
        # print(response.data)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data[0]['region_name'], 'Toshkent')
        self.assertEqual(response.data[0]['id'], 1)
