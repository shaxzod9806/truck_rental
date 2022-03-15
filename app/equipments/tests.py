from django.test import TestCase, Client
from equipments.models import Brand, Category

# from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from index.models import User

from django.contrib.auth import get_user_model

from django.test import Client


class BrandTestCase(TestCase):
    def setUp(self):
        print('(((((((((((((((((((    setUp   )))))))))))))))))))')
        username = "s"
        password = "1"
        user_type = 1
        self.user = get_user_model().objects.create_superuser(username=username, password=password, user_type=user_type)
        jwt_fetch_data = {
            'username': username,
            'password': password,
            user_type: 1
        }
        self.client = APIClient()
        url = ('http://localhost:8000/api/index/login/')
        response = self.client.post(url, jwt_fetch_data)
        # print(response.data)
        # print('&&&&&&&&&&&&&&token&&&&&&&&&&&&&&&&&&&')
        token = response.data['access']
        # print(token)
        # print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
        # self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # print("###############################################################")
        self.Brand = Brand.objects.create(brand_name='TestCase Brand', brand_image=None,
                                          description='TestCase Brand Description')

    def test_get_brand(self):
        print('(((((((((((((((((((    test_get_brand   )))))))))))))))))))')
        response = self.client.get('http://localhost:8000/api/equipments/brands/')
        data = response.data
        # print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['results'][0]['brand_name'], 'TestCase Brand')
        self.assertEqual(data['results'][0]['description'], 'TestCase Brand Description')
        self.assertEqual(data['results'][0]['id'], 1)
        assert (len(data['results']) >= 1)


class CategoryTestCase(TestCase):
    def setUp(self):
        """
        This function is called before each test
        """
        username = "sh"
        password = "2"
        user_type = 1
        self.user = get_user_model().objects.create_superuser(username=username, password=password, user_type=user_type)
        jwt_fetch_data = {
            'username': username,
            'password': password,
            user_type: 1
        }
        self.client = APIClient()
        url = 'http://localhost:8000/api/index/login/'
        response = self.client.post(url, jwt_fetch_data)
        # print(response.data)
        # print('&&&&&&&&&&&&&&token&&&&&&&&&&&&&&&&&&&')
        token = response.data['access']
        # print(token)
        # print("###############################################################")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

        self.Category = Category.objects.create(name_uz='TestCase CategoryUz', name_ru='TestCase CategoryRu',
                                                name_en='TestCase CategoryEn',
                                                description_uz='TestCase Category Description',
                                                description_ru='TestCase Category Description',
                                                description_en='TestCase Category Description',
                                                image=None)

    def test_category_create(self):
        print('(((((((((((((((((((    test_category_create   )))))))))))))))))))')
        response = self.client.get('http://localhost:8000/api/equipments/category/')
        data = response.data
        # print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['results'][0]['name_uz'], 'TestCase CategoryUz')
        self.assertEqual(data['results'][0]['name_ru'], 'TestCase CategoryRu')
        self.assertEqual(data['results'][0]['name_en'], 'TestCase CategoryEn')
        self.assertEqual(data['results'][0]['description_uz'], 'TestCase Category Description')
        self.assertEqual(data['results'][0]['description_ru'], 'TestCase Category Description')
        self.assertEqual(data['results'][0]['description_en'], 'TestCase Category Description')
        self.assertEqual(data['results'][0]['image'], None)
        self.assertEqual(data['results'][0]['id'], 1)
