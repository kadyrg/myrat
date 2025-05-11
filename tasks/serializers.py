from rest_framework import serializers

from .models import Task, Question


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'created_date', 'status']


class QuestionForTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question', 'answer']
        
    
class TaskRetrieveSerializer(serializers.ModelSerializer):
    questions = QuestionForTaskSerializer(many=True)
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'created_date', 'questions', 'status']


class QuestionSerializer(serializers.Serializer):
    question = serializers.CharField(required=True)
