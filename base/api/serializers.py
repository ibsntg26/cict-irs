from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from base.models import Event, News

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