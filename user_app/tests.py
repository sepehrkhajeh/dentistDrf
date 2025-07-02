from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CustomUser


class CustomUserAPITest(APITestCase):
    def setUp(self):
        self.user_data = {
            "phone_number": "09123456789",
            "first_name": "علی",
            "last_name": "محمدی",
            "insurance": "بیمه دی",
            "city": "khorramabad"
        }
        self.user = CustomUser.objects.create(**self.user_data)
        self.list_url = reverse('user-list-create')
        self.detail_url = reverse('user-detail', args=[self.user.pk])

    def test_get_user_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), CustomUser.objects.count())

    def test_get_user_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone_number'], self.user.phone_number)

    def test_update_user(self):
        data = {
            "phone_number": self.user.phone_number,
            "first_name": "رضا",
            "last_name": "محمدی",
            "insurance": "بیمه پاسارگاد",
            "city": "dorud"
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "رضا")

    def test_delete_user(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CustomUser.objects.filter(pk=self.user.pk).exists())

    def test_update_user_with_new_fields(self):
        data = {
            "phone_number": self.user.phone_number,
            "first_name": "رضا",
            "last_name": "محمدی",
            "insurance": "بیمه پاسارگاد",
            "city": "dorud",
            "birth_date": "1370/05/10",
            "history_of_illness": "هیچ بیماری خاصی ندارد"
        }

        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.birth_date, "1370/05/10")
        self.assertEqual(self.user.history_of_illness, "هیچ بیماری خاصی ندارد")
