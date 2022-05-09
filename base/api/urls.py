from django.db import router
from django.urls import path
from rest_framework.routers import DefaultRouter
from . import viewsets

app_name = 'base'
router = DefaultRouter()
router.register(r'event', viewsets.EventViewSet, basename='event')
router.register(r'news', viewsets.NewsViewSet, basename='news')
urlpatterns = router.urls
