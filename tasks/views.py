from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.pagination import PageNumberPagination

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
            answer = "answer"
            Question.objects.create(question=question, answer=answer, task=task)
            return Response({"message": "Question created"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": f"Something went wrong{e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_queryset(self):
        employee = self.request.user
        return Task.objects.filter(employee=employee.id).order_by("-created_date")
    
    def get_serializer_class(self):
        if self.action == "retrieve":
            return TaskRetrieveSerializer
        if self.action == "list":
            return TaskListSerializer
