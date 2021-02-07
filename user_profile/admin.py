from django.contrib import admin

from user_profile.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('profile', 'created_at', 'updated_at',)
