from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status, test


class UserJWTAPiTest(test.APITestCase, TestCase):
    def create_user(self, username='User', password='Pass'):
        return User.objects.create_user(
            username=username,
            password=password,
        )

    def get_jwt_token(self, username='admin', password='adminpass'):
        data = {'username': username, 'password': password}

        url = reverse('user:token_obtain_pair')
        response = self.client.post(url, data=data)

        return response.data

    def test_user_jwt_token_obtain_pair(self):
        data = {'username': 'User', 'password': 'Pass'}
        self.create_user(**data)

        url = reverse('user:token_obtain_pair')
        response = self.client.post(url, data=data)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_user_jwt_token_refresh(self):
        data_user = {'username': 'admin', 'password': 'pass'}
        self.create_user(**data_user)
        refresh = self.get_jwt_token(**data_user).get('refresh')

        url = reverse('user:token_refresh')
        response = self.client.post(url, data={'refresh': refresh})

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_user_jwt_token_verify(self):
        data_user = {'username': 'admin', 'password': 'pass'}
        self.create_user(**data_user)
        access = self.get_jwt_token(**data_user).get('access')

        url = reverse('user:token_verify')
        response = self.client.post(url, data={'token': access})

        self.assertEqual(status.HTTP_200_OK, response.status_code)
