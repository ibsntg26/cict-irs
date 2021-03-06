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
        token['picture'] = user.picture.url

        if token['role'] == 1 or token['role'] == 2:
            token['employee_number'] = user.evaluator.employee_number
        if token['role'] == 3:
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

class UserIncidentInfoSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['picture', 'first_name', 'last_name', 'middle_initial', 'email', 'mobile_number']

class StudentIncidentInfoSerializer(ModelSerializer):
    user = UserIncidentInfoSerializer()
    class Meta:
        model = Student
        fields = ['user', 'student_number', 'section', 'year_level']

class EvaluatorIncidentInfoSerializer(ModelSerializer):
    user = UserIncidentInfoSerializer()
    class Meta:
        model = Evaluator
        fields = ['user', 'employee_number']

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

        user = CustomUser.objects.create_evaluator(**validated_data)
        Evaluator.objects.create(user=user, **data)
        return user

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'picture', 'last_name', 'first_name', 'middle_initial', 'mobile_number', 'evaluator']

class NewStudentSerializer(ModelSerializer):
    student = StudentSerializer()
    password = serializers.CharField(min_length=8, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        domain = email.split('@')[1]
        valid_domains = ['bulsu.edu.ph', 'bulsumain.onmicrosoft.com']

        if domain not in valid_domains :
            raise serializers.ValidationError({'email': 'Email must be a BulSU email.'})
        return attrs

    def create(self, validated_data):
        data = validated_data.pop('student')
        user = CustomUser.objects.create_user(**validated_data)
        Student.objects.create(user=user, **data)
        return user

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'last_name', 'first_name', 'middle_initial', 'mobile_number', 'student']

class UpdateEvaluatorSerializer(ModelSerializer):
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    middle_initial = serializers.CharField(source='user.middle_initial')
    last_name = serializers.CharField(source='user.last_name')
    picture = serializers.ImageField(source='user.picture', allow_empty_file=True, allow_null=True)
    mobile_number = serializers.CharField(source='user.mobile_number')

    class Meta:
        model = Evaluator
        fields = ['email', 'first_name', 'middle_initial', 'last_name', 'picture', 'mobile_number', 'position', 'residential_address']

    def validate(self, attrs):
        new_email = attrs['user'].get('email')

        if new_email is not None:
            domain = new_email.split('@')[1]
            valid_domains = ['bulsumain.onmicrosoft.com']

            if domain not in valid_domains :
                raise serializers.ValidationError({'email': 'Email must be a BulSU email.'})
        return attrs

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')

        instance.user.email = user_data.get('email', instance.user.email)
        instance.user.first_name = user_data.get('first_name', instance.user.first_name)
        instance.user.middle_initial = user_data.get('middle_initial', instance.user.middle_initial)
        instance.user.last_name = user_data.get('last_name', instance.user.last_name)
        if user_data.get('picture') is not None:
            instance.user.picture = user_data.get('picture', instance.user.picture)
        instance.user.mobile_number = user_data.get('mobile_number', instance.user.mobile_number)
        instance.user.save()

        instance.position = validated_data.get('position', instance.position)
        instance.residential_address = validated_data.get('residential_address', instance.residential_address)
        instance.save()
        return instance

class UpdateStudentSerializer(ModelSerializer):
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    middle_initial = serializers.CharField(source='user.middle_initial')
    last_name = serializers.CharField(source='user.last_name')
    picture = serializers.ImageField(source='user.picture', allow_empty_file=True, allow_null=True)
    mobile_number = serializers.CharField(source='user.mobile_number', allow_null=True)

    class Meta:
        model = Student
        fields = ['email', 'first_name', 'middle_initial', 'last_name', 'picture', 'mobile_number', 'year_level', 'section', 'residential_address', 'permanent_address']

    def validate(self, attrs):
        new_email = attrs['user'].get('email')

        if new_email is not None:
            domain = new_email.split('@')[1]
            valid_domains = ['bulsu.edu.ph', 'bulsumain.onmicrosoft.com']

            if domain not in valid_domains :
                raise serializers.ValidationError({'email': 'Email must be a BulSU email.'})
        return attrs

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')

        instance.user.email = user_data.get('email', instance.user.email)
        instance.user.first_name = user_data.get('first_name', instance.user.first_name)
        instance.user.middle_initial = user_data.get('middle_initial', instance.user.middle_initial)
        instance.user.last_name = user_data.get('last_name', instance.user.last_name)
        if user_data.get('picture') is not None:
            instance.user.picture = user_data.get('picture', instance.user.picture)
        instance.user.mobile_number = user_data.get('mobile_number', instance.user.mobile_number)
        instance.user.save()

        instance.year_level = validated_data.get('year_level', instance.year_level)
        instance.section = validated_data.get('section', instance.section)
        instance.residential_address = validated_data.get('residential_address', instance.residential_address)
        instance.permanent_address = validated_data.get('permanent_address', instance.permanent_address)
        instance.save()
        return instance

class IncidentSerializer(ModelSerializer):
    student = StudentIncidentInfoSerializer()
    evaluator = EvaluatorIncidentInfoSerializer()
    class Meta:
        model = Incident
        fields = '__all__'

class NewIncidentSerializer(ModelSerializer):
    class Meta:
        model = Incident
        exclude = ['date_completed']

class ForwardIncidentSerializer(ModelSerializer):
    incident = IncidentSerializer()
    sender = EvaluatorIncidentInfoSerializer()
    receiver = EvaluatorIncidentInfoSerializer()
    class Meta:
        model = ForwardIncident
        fields = '__all__'

class NewForwardIncidentSerializer(ModelSerializer):
    class Meta:
        model = ForwardIncident
        fields = '__all__'

class FollowupSerializer(ModelSerializer):
    user = UserIncidentInfoSerializer()
    incident = IncidentSerializer()
    class Meta:
        model = Followup
        fields = '__all__'

class NewFollowupSerializer(ModelSerializer):
    class Meta:
        model = Followup
        fields = '__all__'

class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class NewEventSerializer(ModelSerializer):
    def validate(self, attrs):
        start = attrs.get('start_date')
        end = attrs.get('end_date')

        if start > end:
            raise serializers.ValidationError({'end_date': 'End date cannot be before start date.'})
        return attrs
    
    class Meta:
        model = Event
        exclude = ['date_created', 'date_updated']

class NewsSerializer(ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

class NewNewsSerializer(ModelSerializer):
    class Meta:
        model = News
        exclude = ['date_created', 'date_updated']
