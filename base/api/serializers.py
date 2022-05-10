from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from base.models import Incident, Followup, Notification


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