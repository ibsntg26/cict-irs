from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from user.models import CustomUser, Evaluator, Student


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