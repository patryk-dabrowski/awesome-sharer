from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from url.models import Resource


class ResourceTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(username='test_user')
        data = {
            "author": self.user,
            "url": "https://example.com"
        }
        self.resource = Resource.objects.create(**data)

    def test_resource_should_expired_after_24_hours(self):
        time = timezone.now() + timezone.timedelta(hours=25)
        self.assertFalse(self.resource.is_available(time))

    def test_resource_should_available_before_24_hours(self):
        time1 = timezone.now() + timezone.timedelta(hours=23)
        time2 = timezone.now() + timezone.timedelta(hours=1)

        self.assertTrue(self.resource.is_available(time1))
        self.assertTrue(self.resource.is_available(time2))
