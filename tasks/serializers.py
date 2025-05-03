from rest_framework import serializers

from .models import Task, Question


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'created_date', 'status']


class TaskRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'created_date', 'status']


class QuestionSerializer(serializers.Serializer):
    question = serializers.CharField(required=True)
