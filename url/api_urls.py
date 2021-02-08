from django.urls import path
from rest_framework import routers

from url.api_views import ShareViewSet, ResourceViewSet, StatisticAPIView

app_name = "url"
router = routers.SimpleRouter()
router.register(r'resource', ResourceViewSet, basename='api_resource')
router.register(r'share', ShareViewSet, basename='api_share')

urlpatterns = [
    path('statistics/', StatisticAPIView.as_view()),
]

urlpatterns += router.urls
