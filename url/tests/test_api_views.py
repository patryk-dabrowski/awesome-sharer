from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase

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
            "slug_url": "codes",
        }
        password = "test"
        resource = Resource(**data)
        resource.set_password(password)
        resource.save()

        response = self.client.get(f'/api/share/{resource.slug_url}/', {"password": password})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"next": resource.redirect_to()})
