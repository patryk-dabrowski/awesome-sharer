from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from url.models import Resource


class ShareViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(username='test_user')
        data = {
            "author": self.user,
            "url": "https://example.com"
        }
        self.resource = Resource.objects.create(**data)

    def test_when_link_expired_should_show_link_expired_message(self):
        self.resource.expired_at = timezone.now() - timezone.timedelta(hours=1)
        self.resource.save()

        response = self.client.get(reverse('share', args=[self.resource.slug_url]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Link expired")

    def test_when_link_still_available_should_show_form_with_input(self):
        response = self.client.get(reverse('share', args=[self.resource.slug_url]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Write a password")
