from django.contrib import admin
from django import forms

from .models import Resource


class ResourceAdminForm(forms.ModelForm):
    plain_password = forms.CharField(required=False)

    class Meta:
        model = Resource
        fields = ('author', 'file', 'url', 'slug_url', 'plain_password', 'created_at', 'expired_at',)

    def clean_plain_password(self):
        plain_password = self.cleaned_data['plain_password']
        if plain_password is not None:
            self.instance.plain_password = plain_password
        return plain_password


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    form = ResourceAdminForm
    list_display = ('author', 'slug_url', 'password',)
