from hashlib import new
from django import views
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework import status
from rest_framework import viewsets
from .serializers import *
from base.models import CustomUser, Evaluator, Student, Incident, Notification
from rest_framework_simplejwt.views import TokenObtainPairView

class AuthTokenViewSet(TokenObtainPairView):
    serializer_class = TokenSerializer

class UserViewSet(viewsets.ViewSet):
    permissions_classes = [AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def list(self, request):
        serializer = UserSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    

# need update, archive
class EvaluatorViewSet(viewsets.ViewSet):
    permissions_classes = [AllowAny]
    queryset = Evaluator.objects.all()
    serializer_class = NewEvaluatorSerializer

    def list(self, request):
        serializer = EvaluatorInfoSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def update(self, request, pk=None):
    #     pass

    def retrieve(self, request, pk=None):
        evaluator = get_object_or_404(self.queryset, pk=pk)
        serializer = EvaluatorInfoSerializer(evaluator, many=False)
        return Response(serializer.data)

# need update, archive
class StudentViewSet(viewsets.ViewSet):
    permissions_classes = [AllowAny]
    queryset = Student.objects.all()
    serializer_class = NewStudentSerializer

    def list(self, request):
        serializer = StudentInfoSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def update(self, request, pk=None):
    #     pass

    def retrieve(self, request, pk=None):
        student = get_object_or_404(self.queryset, pk=pk)
        serializer = StudentInfoSerializer(student, many=False)
        return Response(serializer.data)

class AllIncidentViewset(viewsets.ViewSet):
    permission_classes = [AllowAny]
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        incident = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(incident, many=False)
        return Response(serializer.data)

class StudentIncidentViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    queryset = Incident.objects.all()
    serializer_class = NewIncidentSerializer

    def list(self, request):
        student = Student.objects.get(user=request.user)
        incidents = self.queryset.filter(student=student)
        serializer = IncidentSerializer(incidents, many=True)
        return Response(serializer.data)

    def create(self, request):
        student = Student.objects.get(user=request.user)
        new_data = request.data.copy()
        new_data.update({'student':student.student_number})

        serializer = self.serializer_class(data=new_data)
        serializer.is_valid(raise_exception=True)
        incident = serializer.save()

        Notification.objects.create(
            incident=incident,
            user = incident.student.user,
            subject = 'Incident Submitted!',
            message = ''
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        incident = get_object_or_404(self.queryset, pk=pk)
        serializer = IncidentSerializer(incident, many=False)
        return Response(serializer.data)

    # def partial_update(self, request, pk=None):
    #     incident = get_object_or_404(self.queryset, pk=pk)
    #     data = request.data
    #     action = data['action']

    #     if action == 'process':
    #         try:
    #             evaluator = data['evaluator_id']
    #             incident.evaluator_id = evaluator
    #             incident.status = 'In Progress'
    #             incident.save()
    #         except Exception:
    #             return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)
    #     elif action == 'close':
    #         incident.status = 'Resolved'
    #         incident.save()
    #     return Response({'success': True})

class FollowupViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    queryset = Followup.objects.all()
    serializer_class = FollowupSerializer

    def list(self, request):
        incident = request.GET.get('incident')

        if incident is not None:
            serializer = self.serializer_class(self.queryset.filter(incident_id=incident), many=True)
        else:
            serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        followup = serializer.save()

        # Notification.objects.create(
        #     incident=followup,
        #     user = followup.student.user,
        #     subject = 'Feedback Received',
        #     message = 'Message goes here.'
        # )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        followup = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(followup, many=False)
        return Response(serializer.data)

class NotificationViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def list(self, request):
        user = request.GET.get('user')
        notifications = self.queryset

        if user is not None:
            serializer = self.serializer_class(notifications.filter(user_id=user), many=True)
        else:
            serializer = self.serializer_class(notifications, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        notif = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(notif, many=False)
        return Response(serializer.data)

class EventViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    queryset = Event.objects.all()
    serializer_class = NewEventSerializer

    def list(self, request):
        serializer = EventSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        event = get_object_or_404(self.queryset, pk=pk)
        serializer = EventSerializer(event, many=False)
        return Response(serializer.data)

class NewsViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        news = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(news, many=False)
        return Response(serializer.data)