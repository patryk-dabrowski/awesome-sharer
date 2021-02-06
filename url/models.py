from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from url.crypter import Crypter
from url.generator import Generator


class Resource(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    file = models.FileField(blank=True)
    url = models.URLField(blank=True)
    slug_url = models.SlugField(unique=True, null=True, default=Generator.generate)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(default=timezone.now)
    expired_at = models.DateTimeField(blank=True)

    def __str__(self):
        return f"{self.slug_url} ({self.author})"

    def clean(self):
        if not self.expired_at:
            self.expired_at = timezone.now() + timezone.timedelta(hours=24)

    def set_password(self, value: str):
        self.password = Crypter(value).encrypt()

    def check_password(self, password: str) -> bool:
        return Crypter(password).equals(self.password)
