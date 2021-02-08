from rest_framework import routers

from url.api_views import ShareViewSet, ResourceViewSet

app_name = "url"
router = routers.SimpleRouter()
router.register(r'resource', ResourceViewSet, basename='api_resource')
router.register(r'share', ShareViewSet, basename='api_share')

urlpatterns = router.urls
