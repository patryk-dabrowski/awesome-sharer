from django.contrib.auth import get_user_model
from django.db import models


class UserProfile(models.Model):
    profile = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, primary_key=True, related_name='profile')
    meta_data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.profile}"
