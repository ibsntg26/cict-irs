from django.db import router
from django.urls import path
from rest_framework.routers import DefaultRouter
from . import viewsets

app_name = 'base'
router = DefaultRouter()
router.register(r'incident', viewsets.IncidentViewSet, basename='incident')
router.register(r'followup', viewsets.FollowupViewSet, basename='followup')
router.register(r'notification', viewsets.NotificationViewSet, basename='notification')
urlpatterns = router.urls
