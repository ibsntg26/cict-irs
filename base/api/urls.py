from django.db import router
from django.urls import path
from rest_framework.routers import DefaultRouter
from . import viewsets

app_name = 'base'
router = DefaultRouter()

router.register(r'user', viewsets.UserViewSet, basename='user')
router.register(r'evaluator', viewsets.EvaluatorViewSet, basename='evaluator')
router.register(r'student', viewsets.StudentViewSet, basename='student')
router.register(r'incident', viewsets.IncidentViewSet, basename='incident')
router.register(r'followup', viewsets.FollowupViewSet, basename='followup')
router.register(r'notification', viewsets.NotificationViewSet, basename='notification')
router.register(r'event', viewsets.EventViewSet, basename='event')
router.register(r'news', viewsets.NewsViewSet, basename='news')
urlpatterns = router.urls
