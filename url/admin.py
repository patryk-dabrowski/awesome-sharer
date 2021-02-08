from django import forms
from django.contrib import admin

from .generator import Generator
from .models import Resource


class ResourceAdminForm(forms.ModelForm):
    plain_password = forms.CharField(required=False)

    class Meta:
        model = Resource
        fields = ('author', 'file', 'url', 'slug_url', 'plain_password', 'created_at', 'expired_at',)

    def clean_plain_password(self):
        plain_password = self.cleaned_data['plain_password']
        if plain_password is not None:
            self.instance.set_password(plain_password)
        elif not self.instance.password:
            self.instance.set_password(Generator.generate(5))
        return plain_password


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    form = ResourceAdminForm
    list_display = ('author', 'slug_url', 'password',)
