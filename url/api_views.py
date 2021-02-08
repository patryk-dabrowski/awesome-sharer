from django.urls import reverse
from rest_framework import generics, viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from url.generator import Generator
from url.models import Resource
from url.permissions import IsPermitted
from url.serializers import ResourceSerializer, ResourceDetailSerializer, ShareResourceSerializer


class ResourceViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)

        password = Generator.generate(5)
        instance.set_password(password)
        instance.save()

        data = {
            "password": password,
            "path": request.build_absolute_uri(reverse('share', args=[instance.slug_url]))
        }

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class ShareViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    lookup_field = 'slug_url'
    lookup_value_regex = '[0-9a-zA-Z]{5}'
    lookup_url_kwarg = 'slug_url'
    queryset = Resource.objects.all()
    serializer_class = ShareResourceSerializer
    permission_classes = (IsPermitted,)
