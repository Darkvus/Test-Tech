# -*- coding: utf-8 -*-

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import ApiViewSet

router = DefaultRouter()
router.register(r'', ApiViewSet, basename='api')

urlpatterns = [
    path('', include(router.urls)),
]
