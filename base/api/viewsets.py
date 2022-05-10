from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework import status
from rest_framework import viewsets
from .serializers import *


# class EventViewSet(viewsets.ViewSet):
#     permission_classes = [AllowAny]
#     queryset = Event.objects.all()
#     serializer_class = NewEventSerializer

#     def list(self, request):
#         serializer = EventSerializer(self.queryset, many=True)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def retrieve(self, request, pk=None):
#         event = get_object_or_404(self.queryset, pk=pk)
#         serializer = EventSerializer(event, many=False)
#         return Response(serializer.data)

# class NewsViewSet(viewsets.ViewSet):
#     permission_classes = [AllowAny]
#     queryset = News.objects.all()
#     serializer_class = NewsSerializer

#     def list(self, request):
#         serializer = self.serializer_class(self.queryset, many=True)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def retrieve(self, request, pk=None):
#         news = get_object_or_404(self.queryset, pk=pk)
#         serializer = self.serializer_class(news, many=False)
#         return Response(serializer.data)