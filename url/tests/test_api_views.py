from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from rest_framework.test import APITestCase

from url.generator import Generator
from url.models import Resource


class ResourceViewSetTest(APITestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(username='test_user')

    def test_anonymous_user_should_raise_error(self):
        payload = {}
        response = self.client.post('/api/resource/', payload, format='multipart')

        self.assertEqual(response.status_code, 401)

    def test_create_new_resource_without_params_should_raise_error(self):
        self._login_user()
        payload = {}
        response = self.client.post('/api/resource/', payload, format='multipart')

        self.assertEqual(response.status_code, 400)

    def test_create_new_resource_with_file(self):
        self._login_user()

        file = SimpleUploadedFile("test.txt", b'abc', content_type='text/plain')
        payload = {
            "file": file
        }
        response = self.client.post('/api/resource/', payload, format='multipart')

        self.assertEqual(response.status_code, 201)
        self.assertCountEqual(response.data.keys(), ['path', 'password'])
        self.assertTrue(Resource.objects.count() > 0)

    def test_create_new_resource_with_url(self):
        self._login_user()

        payload = {
            "url": "https://example.com"
        }
        response = self.client.post('/api/resource/', payload, format='multipart')

        self.assertEqual(response.status_code, 201)
        self.assertCountEqual(response.data.keys(), ['path', 'password'])
        self.assertTrue(Resource.objects.count() > 0)

    def _login_user(self):
        self.client.force_authenticate(user=self.user)


class ShareViewSetTest(APITestCase):
    def test_fetch_protected_resource_with_invalid_password_should_raise_error(self):
        user = get_user_model().objects.create(username='test_user')

        data = {
            "author": user,
            "url": "https://example.com",
            "slug_url": "codescodes",
        }
        resource = Resource(**data)
        resource.set_password("test")
        resource.save()

        response = self.client.get(f'/api/share/{resource.slug_url}/', {"password": "test2"})
        self.assertEqual(response.status_code, 401)

    def test_fetch_protected_resource(self):
        user = get_user_model().objects.create(username='test_user')

        data = {
            "author": user,
            "url": "https://example.com",
            "slug_url": "codescodes",
        }
        password = "test"
        resource = Resource(**data)
        resource.set_password(password)
        resource.save()

        response = self.client.get(f'/api/share/{resource.slug_url}/', {"password": password})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"next": resource.redirect_to()})


class StatisticAPIViewTest(APITestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(username='test_user')
        self.user2 = get_user_model().objects.create(username='test_user2')

    def test_reject_anonymous_access(self):
        response = self.client.get('/api/statistics/')
        self.assertEqual(response.status_code, 401)

    def test_generate_statistic(self):
        self.client.force_authenticate(user=self.user)
        self._generate_data(self.user)

        response = self.client.get('/api/statistics/')

        self.assertEqual(response.status_code, 200)
        expected = {
            "2017-10-25": {
                "files": 1,
                "links": 1
            },
            "2017-10-26": {
                "files": 1,
                "links": 0
            },
        }
        self.assertDictEqual(response.data, expected)

    def test_generate_statistic_only_for_current_user(self):
        self.client.force_authenticate(user=self.user)
        self._generate_data(self.user)
        self._generate_data(self.user2)

        response = self.client.get('/api/statistics/')

        self.assertEqual(response.status_code, 200)
        expected = {
            "2017-10-25": {
                "files": 1,
                "links": 1
            },
            "2017-10-26": {
                "files": 1,
                "links": 0
            },
        }
        self.assertDictEqual(response.data, expected)

    def _generate_data(self, user):
        date1 = timezone.datetime(2017, 10, 25, tzinfo=timezone.utc)
        date2 = date1 + timezone.timedelta(days=1)
        simple_file = SimpleUploadedFile("test.txt", b'abc', content_type='text/plain')
        simple_url = "https://example.com"
        resource_data = [
            (date1, 5, simple_file, ""),
            (date1, 2, None, simple_url),
            (date2, 2, simple_file, ""),
            (date2, 0, simple_file, ""),
            (date2, 0, None, simple_url),
        ]
        [self._create_resource(user, *rd) for rd in resource_data]

    def _create_resource(self, user, created_at=timezone.now(), visits=0, file=None, url=None):
        data = {
            "author": user,
            "url": url,
            "file": file,
            "slug_url": Generator.generate(10),
            "created_at": created_at,
            "visits": visits
        }
        resource = Resource(**data)
        resource.set_password("test")
        resource.save()
