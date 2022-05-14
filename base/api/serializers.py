from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from base.models import *


class TokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['name'] = f'{user.first_name} {user.last_name}'
        token['role'] = user.role

        if token['role'] == 1 or token['role'] == 2:
            token['employee_number'] = user.evaluator.employee_number
        if token['role'] == 'student':
            token['student_number'] = user.student.student_number
        return token

class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ['password']

class EvaluatorInfoSerializer(ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Evaluator
        fields = '__all__'

class StudentInfoSerializer(ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Student
        fields = '__all__'

class EvaluatorSerializer(ModelSerializer):
    class Meta:
        model = Evaluator
        exclude = ['user']

class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        exclude = ['user']

class NewEvaluatorSerializer(ModelSerializer):
    evaluator = EvaluatorSerializer()
    password = serializers.CharField(min_length=8, write_only=True)
    picture = serializers.ImageField(allow_empty_file=True, allow_null=True)

    def validate(self, attrs):
        email = attrs.get('email')
        domain = email.split('@')[1]
        valid_domains = ['bulsu.edu.ph', 'bulsumain.onmicrosoft.com']

        if domain not in valid_domains :
            raise serializers.ValidationError({'email': 'email must be a valid BulSU email.'})
        return attrs

    def create(self, validated_data):
        data = validated_data.pop('evaluator')
        picture = validated_data['picture']

        if picture is None:
            validated_data.pop('picture')

        user = CustomUser.objects.create_user(**validated_data)
        Evaluator.objects.create(user=user, **data)
        return user

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'picture', 'last_name', 'first_name', 'middle_initial', 'mobile_number', 'evaluator']

class NewStudentSerializer(ModelSerializer):
    student = StudentSerializer()
    password = serializers.CharField(min_length=8, write_only=True)
    picture = serializers.ImageField(allow_empty_file=True, allow_null=True)

    def validate(self, attrs):
        email = attrs.get('email')
        domain = email.split('@')[1]
        valid_domains = ['bulsu.edu.ph', 'bulsumain.onmicrosoft.com']

        if domain not in valid_domains :
            raise serializers.ValidationError({'email': 'email must be a valid BulSU email.'})
        return attrs

    def create(self, validated_data):
        data = validated_data.pop('student')
        picture = validated_data['picture']

        if picture is None:
            validated_data.pop('picture')

        user = CustomUser.objects.create_user(**validated_data)
        Student.objects.create(user=user, **data)
        return user

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'picture', 'last_name', 'first_name', 'middle_initial', 'mobile_number', 'student']

class IncidentSerializer(ModelSerializer):
    class Meta:
        model = Incident
        fields = '__all__'

class NewIncidentSerializer(ModelSerializer):
    class Meta:
        model = Incident
        exclude = ['date_completed']

class FollowupSerializer(ModelSerializer):
    class Meta:
        model = Followup
        fields = '__all__'

class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'












# class IncidentSerializer(ModelSerializer):
#     class Meta:
#         model = Incident
#         fields = '__all__'

# class NewIncidentSerializer(ModelSerializer):
#     class Meta:
#         model = Incident
#         exclude = ['date_completed']

# class FollowupSerializer(ModelSerializer):
#     class Meta:
#         model = Followup
#         fields = '__all__'

# class NotificationSerializer(ModelSerializer):
#     class Meta:
#         model = Notification
#         fields = '__all__'