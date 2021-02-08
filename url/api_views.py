from collections import defaultdict

from django.db.models import Count
from django.urls import reverse
from rest_framework import generics, viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
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
    lookup_value_regex = '[0-9a-zA-Z]{10}'
    lookup_url_kwarg = 'slug_url'
    queryset = Resource.objects.all()
    serializer_class = ShareResourceSerializer
    permission_classes = (IsPermitted,)


class StatisticAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, *args, **kwargs):
        resources = (Resource.objects.filter(author=self.request.user, visits__gt=0)
                     .values('created_at', 'file', 'url')
                     .order_by('created_at'))
        data = defaultdict(lambda: {"files": 0, "links": 0})
        for resource in resources:
            created_at = resource.get('created_at').strftime('%Y-%m-%d')
            file = resource.get('file')
            url = resource.get('url')
            if file:
                data[created_at]['files'] += 1
            if url:
                data[created_at]['links'] += 1

        return Response(data)
