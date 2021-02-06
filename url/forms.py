from django import forms
from django.core.exceptions import ValidationError

from .models import Resource


class ResourceForm(forms.ModelForm):
    file = forms.FileField(required=False)
    url = forms.URLField(required=False)

    class Meta:
        model = Resource
        fields = ('file', 'url',)

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('file') and not cleaned_data.get('url'):
            raise ValidationError({'file': 'Field is required', 'url': 'Field is required'})
        return cleaned_data


class ShareResourceForm(forms.ModelForm):
    plain_password = forms.CharField(required=True, label="Write a password")

    class Meta:
        model = Resource
        fields = ('plain_password',)

    def clean(self):
        cleaned_data = super().clean()
        if not self.instance.check_password(cleaned_data.get('plain_password')):
            raise ValidationError({'plain_password': "Password doesn't match :("})
        return cleaned_data
