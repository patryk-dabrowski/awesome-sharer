from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


class Resource(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    file = models.FileField(blank=True)
    url = models.URLField(blank=True)
    slug_url = models.SlugField(unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(default=timezone.now)
    expired_at = models.DateTimeField(blank=True)

    def __str__(self):
        return f"{self.slug_url} ({self.author})"

    def clean(self):
        if not self.expired_at:
            self.expired_at = timezone.now() + timezone.timedelta(hours=24)

    @property
    def plain_password(self):
        return self.password

    @plain_password.setter
    def plain_password(self, value):
        self.password = value

    def check_password(self, password):
        return self.password == password
