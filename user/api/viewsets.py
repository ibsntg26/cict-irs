from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework import status
# # from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets
from .serializers import *
from user.models import CustomUser, Evaluator, Student


# # https://youtu.be/dCbfOZurCQk?t=574
# # https://www.django-rest-framework.org/api-guide/viewsets/

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


