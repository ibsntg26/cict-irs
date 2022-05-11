from django import views
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework import status
from rest_framework import viewsets
from .serializers import IncidentSerializer, NewIncidentSerializer, FollowupSerializer, NotificationSerializer
from base.models import Incident, Followup, Notification


class IncidentViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    queryset = Incident.object.all()
    serializer_class = NewIncidentSerializer

    def list(self, request):
        student = request.GET.get('student')
        evaluator = request.GET.get('evaluator')
        incidents = self.queryset

        if student is not None:
            serializer = IncidentSerializer(incidents.filter(student_id=student), many=True)
        elif evaluator is not None:
            serializer = IncidentSerializer(incidents.filter(evaluator_id=evaluator), many=True)
        else:
            serializer = IncidentSerializer(incidents, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Notification.objects.create(
        #     incident=incident,
        #     user_id = incident.user_id,
        #     subject = incident.report_type,
        #     message = ''
        # )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        incident = get_object_or_404(self.queryset, pk=pk)
        serializer = IncidentSerializer(incident, many=False)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        incident = get_object_or_404(self.queryset, pk=pk)
        data = request.data
        action = data['action']

        if action == 'process':
            try:
                evaluator = data['evaluator_id']
                incident.evaluator_id = evaluator
                incident.status = 'In Progress'
                incident.save()
            except Exception:
                return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)
        elif action == 'close':
            incident.status = 'Resolved'
            incident.save()
        return Response({'success': True})

class FollowupViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    queryset = Followup.object.all()
    serializer_class = FollowupSerializer

    def list(self, request):
        incident = request.GET.get('incident')

        if incident is not None:
            serializer = self.serializer_class(self.queryset.filter(incident_id=incident))
        else:
            serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        followup = serializer.save()

        # Notification.objects.create(
        #     incident=followup,
        #     user_id = incident.user_id,
        #     subject = incident.report_type,
        #     message = ''
        # )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        followup = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(followup, many=False)
        return Response(serializer.data)

class NotificationViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    queryset = Notification.object.all()
    serializer_class = NotificationSerializer

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        notif = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(notif, many=False)
        return Response(serializer.data)