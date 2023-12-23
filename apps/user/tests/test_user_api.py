from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status, test


class UserApiTest(test.APITestCase, TestCase):
    def create_user(self, username='User', password='Pass'):
        return User.objects.create_user(
            username=username,
            password=password,
        )

    def get_jwt_token(self, username='User', password='Pass'):
        data = {'username': username, 'password': password}

        url = reverse('user:token_obtain_pair')
        response = self.client.post(url, data=data)

        access = response.data.get('access')
        bearer = f'Bearer {access}'

        return bearer

    def test_user_me_list_status_code_200_OK(self):
        data = {'username': 'User', 'password': 'Pass'}

        self.create_user(**data)
        access = self.get_jwt_token(**data)

        url = reverse('user:user-api-list')
        response = self.client.get(url, HTTP_AUTHORIZATION=access)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_user_me_detail_status_code_200_OK(self):
        data = {'username': 'User', 'password': 'Pass'}

        user = self.create_user(**data)
        access = self.get_jwt_token(**data)

        url = reverse('user:user-api-detail', args=(user.id,))
        response = self.client.get(url, HTTP_AUTHORIZATION=access)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_user_me_detail_status_code_403_FORBIDDEN(self):
        data = {'username': 'User', 'password': 'Pass'}

        self.create_user(**data)
        another_user = self.create_user('AnotherUser', 'AnotherPass')
        access = self.get_jwt_token(**data)

        url = reverse('user:user-api-detail', args=(another_user.id,))
        response = self.client.get(url, HTTP_AUTHORIZATION=access)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
