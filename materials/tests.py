from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from materials.models import Well, Lesson, Subscription
from users.models import User


class WellTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@example.com")
        self.well = Well.objects.create(name="Физика", description="Школьный курс", owner=self.user)
        self.lesson = Lesson.objects.create(name="Квантовая физика", description="Раздел физики", well=self.well)
        self.client.force_authenticate(user=self.user)

    def test_well_retrieve(self):
        """ Тест на просмотр одного курса """

        url = reverse("materials:well-detail", args=(self.well.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), self.well.name
        )

    def test_well_create(self):
        """ Тест на создания курса """

        url = reverse("materials:well-list")
        data = {
            "name": "Биология"
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Well.objects.all().count(), 2
        )

    def test_well_update(self):
        """ Тест на изменения курса """

        url = reverse("materials:well-detail", args=(self.well.pk,))
        data = {
            "name": "Литература"
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), "Литература"
        )

    def test_well_delete(self):
        """ Тест на удаление курса """

        url = reverse("materials:well-detail", args=(self.well.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Well.objects.all().count(), 0
        )

    def test_well_list(self):
        """ Тест на вывод списка курса """

        url = reverse("materials:well-list")
        response = self.client.get(url)
        data = response.json()
        result = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.well.pk,
                    'lessons': [
                        {
                            'id': self.lesson.pk,
                            'name': self.lesson.name,
                            'description': self.lesson.description,
                            'preview': None,
                            'link_to_video': None,
                            'well': self.well.pk,
                            'owner': None
                        }
                    ],
                    'name': self.well.name,
                    'preview': None,
                    'description': self.well.description,
                    'owner': self.user.pk
                }
            ]
        }
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, result
        )


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@example.com")
        self.well = Well.objects.create(name="Физика", description="Школьный курс", owner=self.user)
        self.lesson = Lesson.objects.create(
            name="Квантовая физика", description="Раздел физики", well=self.well, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        """ Тест на просмотр одного урока """
        url = reverse("materials:lessons_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), self.lesson.name
        )

    def test_lesson_create(self):
        """ Тест на создание урока """

        url = reverse("materials:lessons_create")
        data = {
            "name": "Механика"
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.all().count(), 2
        )

    def test_lesson_update(self):
        """ Тест на изменение урока """

        url = reverse("materials:lessons_update", args=(self.lesson.pk,))
        data = {
            "name": "Атомная физика"
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), "Атомная физика"
        )

    def test_lesson_delete(self):
        """ Тест на удаление урока """

        url = reverse("materials:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

    def test_lesson_list(self):
        """ Тест на вывод списка уроков """

        url = reverse("materials:lessons_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.lesson.pk,
                    'name': self.lesson.name,
                    'description': self.lesson.description,
                    'preview': None,
                    'link_to_video': None,
                    'well': self.well.pk,
                    'owner': self.user.pk
                }
            ]
        }
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, result
        )

class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@example.com")
        self.well = Well.objects.create(name="Физика", description="Школьный курс", owner=self.user)
        self.lesson = Lesson.objects.create(
            name="Квантовая физика", description="Раздел физики", well=self.well, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_subscription_create(self):
        """ Тест на создание подписки """

        url = reverse('materials:subscription_create')
        data = {
            'user': self.user,
            'well': self.well.pk
        }
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, {'message': 'подписка добавлена'}
        )

    def test_subscription_delete(self):
        """ Тест на удаление подписки """

        self.subscription = Subscription.objects.create(user=self.user, well=self.well)
        url = reverse('materials:subscription_create')
        data = {
            'user': self.user,
            'well': self.well.pk
        }
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, {'message': 'подписка удалена'}
        )
