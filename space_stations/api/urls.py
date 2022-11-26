from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers

from .views import StationViewSet

app_name = 'api'

router = routers.DefaultRouter()

router.register('stations', StationViewSet, basename='stations')


urlpatterns = [
    path('', include(router.urls)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'schema/swagger/',
        SpectacularSwaggerView.as_view(url_name='api:schema'),
        name='swagger'
    ),
]
