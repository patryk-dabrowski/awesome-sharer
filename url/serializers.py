from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from url.models import Resource


class ResourceSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=False)
    url = serializers.URLField(required=False)

    class Meta:
        model = Resource
        fields = ('file', 'url',)

    def validate(self, attrs):
        if not attrs.get('file') and not attrs.get('url'):
            missing_items = {
                'file': _('This field is required.'),
                'url': _('This field is required.')
            }
            raise serializers.ValidationError(missing_items, code='required')
        return attrs


class ResourceDetailSerializer(serializers.ModelSerializer):
    path = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = Resource
        fields = ('path', 'password',)


class ShareResourceSerializer(serializers.ModelSerializer):
    next = serializers.SerializerMethodField()

    class Meta:
        model = Resource
        fields = ('next',)

    def get_next(self, obj: Resource):
        return obj.redirect_to()
