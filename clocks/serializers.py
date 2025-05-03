from rest_framework import serializers

from .models import Clock


class ClockListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clock
        fields = ['id', "started_date", "ended_date", "duration", "status"]


class ClockRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clock
        fields = ['id', "started_date", "ended_date", "duration", "status"]
