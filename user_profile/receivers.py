from django.dispatch import receiver

from url.signals import update_user_meta
from user_profile.models import UserProfile


@receiver(update_user_meta)
def update_user_agent(**kwargs):
    request = kwargs.get('request')
    user_agent = request.META['HTTP_USER_AGENT']
    user = request.user

    profile, _ = UserProfile.objects.get_or_create(profile=user)
    profile.meta_data = user_agent
    profile.save()
