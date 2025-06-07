from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.pagination import PageNumberPagination
from openai import OpenAI

from .models import Task, Question
from .serializers import TaskListSerializer, TaskRetrieveSerializer, QuestionSerializer
from accounts.models import User


class TaskPagination(PageNumberPagination):
    page_size_query_param = 'page_size'

class TaskViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    pagination_class = TaskPagination
    
    @action(methods=['post'], detail=True, url_path='start_task')
    def start_task(self, *args, **kwargs):
        employee = self.request.user
        task_id = kwargs.get('pk')
        task = Task.objects.filter(id=task_id, employee=employee.pk).first()
        if not User.objects.filter(id=employee.id).first():
            return Response({"detail": "Employee does not exist"}, status=status.HTTP_401_UNAUTHORIZED)
        if not task:
            return Response({"detail": "Task with this id does not exist"}, status=status.HTTP_404_NOT_FOUND)
        if task.status == "active":
            return Response({"detail": f"Task {task_id} already started"}, status=status.HTTP_400_BAD_REQUEST)
        # if task.status == "deactive":
        task.start_task()
        return Response({"message": f"Task {task_id} started"}, status=status.HTTP_200_OK)
        # return Response({"detail": f"Task {task_id} cannot be started"}, status=status.HTTP_400_BAD_REQUEST)
    
    
    @action(methods=['post'], detail=True, url_path='end_task')
    def end_task(self, *args, **kwargs):
        employee = self.request.user
        task_id = kwargs.get('pk')
        task = Task.objects.filter(id=task_id, employee=employee.pk).first()
        if not User.objects.filter(id=employee.id).first():
            return Response({"detail": "Employee does not exist"}, status=status.HTTP_401_UNAUTHORIZED)
        if not task:
            return Response({"detail": "Task with this id does not exist"}, status=status.HTTP_404_NOT_FOUND)
        if task.status == "success":
            return Response({"detail": f"Task {task_id} already finished"}, status=status.HTTP_400_BAD_REQUEST)
        # if task.status == "active":
        task.end_task()
        return Response({"message": f"Task {task_id} ended"}, status=status.HTTP_200_OK)
        # return Response({"detail": f"Task {task_id} cannot be ended"})


    @action(methods=['post'], detail=True, url_path='decline_task')
    def decline_task(self, *args, **kwargs):
        employee = self.request.user
        task_id = kwargs.get('pk')
        task = Task.objects.filter(id=task_id, employee=employee.pk).first()
        if not User.objects.filter(id=employee.id).first():
            return Response({"detail": "Employee does not exist"}, status=status.HTTP_401_UNAUTHORIZED)
        if not task:
            return Response({"detail": "Task with this id does not exist"}, status=status.HTTP_404_NOT_FOUND)
        if task.status == "declined":
            return Response({"detail": f"Task {task_id} already declined"}, status=status.HTTP_400_BAD_REQUEST)
        # if task.status == "active":
        task.decline_task()
        return Response({"message": f"Task {task_id} declined"}, status=status.HTTP_200_OK)
        # return Response({"detail": f"Task {task_id} cannot be declined"})


    @action(methods=['post'], detail=True, url_path='fail_task')
    def fail_task(self, *args, **kwargs):
        employee = self.request.user
        task_id = kwargs.get('pk')
        task = Task.objects.filter(id=task_id, employee=employee.pk).first()
        if not User.objects.filter(id=employee.id).first():
            return Response({"detail": "Employee does not exist"}, status=status.HTTP_401_UNAUTHORIZED)
        if not task:
            return Response({"detail": "Task with this id does not exist"}, status=status.HTTP_404_NOT_FOUND)
        # if task.status == "active":
        if task.status == "failed":
            return Response({"detail": f"Task {task_id} already failed"}, status=status.HTTP_400_BAD_REQUEST)
        task.fail_task()
        return Response({"message": f"Task {task_id} failed"}, status=status.HTTP_200_OK)
        # return Response({"detail": f"Task {task_id} cannot be failed"})


    @swagger_auto_schema(
        method='post',
        request_body=QuestionSerializer,
        responses={200: 'OK'}
    )
    @action(methods=['post'], detail=True, url_path='ask')
    def ask(self, request, pk=None):
        serializer = QuestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        question = serializer.validated_data['question']
        
        employee = request.user
        task = Task.objects.filter(id=pk, employee=employee.pk).first()
        
        if not User.objects.filter(id=employee.id).first():
            return Response({"detail": "Employee does not exist"}, status=status.HTTP_401_UNAUTHORIZED)
        if not task:
            return Response({"detail": "Task with this id does not exist"}, status=status.HTTP_404_NOT_FOUND)
        if task.status != "active":
            return Response({"message": f"Task {pk} must be started"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            client = OpenAI(api_key="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")
            system_prompt = f"You are an assistant helping with the task: '{task.title}'. Answer questions based on this task context."
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question},
                ],
                stream=False
            )
            answer = response.choices[0].message.content
            question = Question.objects.create(question=question, answer=answer, task=task)
            
            return Response({
                "id": question.id,
                "question": question.question,
                "answer": question.answer,
                "task": question.task.id
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": f"Something went wrong{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_queryset(self):
        employee = self.request.user
        return Task.objects.filter(employee=employee.id).order_by("-created_date")
    
    def get_serializer_class(self):
        if self.action == "retrieve":
            return TaskRetrieveSerializer
        if self.action == "list":
            return TaskListSerializer
