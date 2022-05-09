from django.urls import path
from rest_framework.routers import DefaultRouter
from . import viewsets
from rest_framework_simplejwt.views import TokenRefreshView


app_name = 'user'
router = DefaultRouter()
router.register(r'evaluator', viewsets.EvaluatorViewSet, basename='evaluator')
router.register(r'student', viewsets.StudentViewSet, basename='student')
urlpatterns = router.urls
