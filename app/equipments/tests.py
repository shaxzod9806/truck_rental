from django.test import TestCase, Client
from equipments.models import Brand, Category

# from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from index.models import User

# import pytest
#
#
# @pytest.fixture
# def api_client(username, password, user_type):
#     user = User.objects.create_user(username=username, password=password, user_type=user_type)
#     client = APIClient()
#     refresh = RefreshToken.for_user(user)
#     print(refresh)
#     client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
#     return client

from django.test import Client


class BrandTestCase(TestCase):
    def setUp(self):
        # self.client = Client(username="s", password="1")
        # token = self.client.post('http://localhost:8000/api/index/login/',
        #                           http: // localhost: 8000 / api / index / login /

        #                          {'username': 's', 'password': '1'})

        username = "+998931209806111"
        password = "string98"
        self.user = User.objects.create_user(username, username, password)
        jwt_fetch_data = {
            'username': username,
            'password': password
        }

        url = ('http://localhost:8000/api/index/login/')
        response = self.client.post(url, jwt_fetch_data, format='json')
        token = response.data['access']
        print(token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        print("###############################################################")
        self.Brand = Brand.objects.create(brand_name='TestCase Brand')

    def test_get_brand(self):
        response = self.client.get('http://localhost:8000/api/equipments/brands/')
        data = response.data
        # print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['results'][0]['brand_name'], 'TestCase Brand')
        self.assertEqual(data['results'][0]['id'], 1)
        assert (len(data['results']) >= 1)

#     def test_post_brand(self):
#         response = self.client.post('http://localhost:8000/api/equipments/brands/',
#                                     {'brand_name': 'TestCase post Brand'})
#         data = response.data
#         # print(data)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(data['brand_name'], 'TestCase post Brand')
#
#
# class CategoryTestCase(TestCase):
#     def setUp(self):
#         self.client = Client(username="admin", password="a3qwGW4KHD")
#
#         token = self.client.post('http://localhost:8000/api/index/login/',
#                                  {'username': 'admin', 'password': 'a3qwGW4KHD'})
#         print(token)
#         # self.client = Client()
#         self.client.login(username='admin', password="a3qwGW4KHD")
#         self.Category = Category.objects.create(name_uz='TestCase Category', name_ru='TestCase Category')
#
#     def test_get_category(self):
#         self.client = User.objects.create(username='+998931209806',password='a3qwGW4KHD',user_type=4)
#         response = self.client.get('https://api.motochas.uz/api/equipments/category/')
#         data = response.data
#         # print(data)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(data['results'][0]['name_uz'], 'TestCase Category')
#         self.assertEqual(data['results'][0]['id'], 1)
#         assert (len(data['results']) >= 1)
#
#     def test_post_category(self):
#         response = self.client.post('https://api.motochas.uz/api/equipments/category/',
#                                     {'name_uz': 'TestCase post Category', 'name_ru': 'TestCase post Category'})
#         data = response.data
#         # print(data)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(data['category_name'], 'TestCase post Category')
