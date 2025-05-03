from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Task, Question
from .serializers import TaskListSerializer, TaskRetrieveSerializer
from accounts.models import User


class TaskViewSet(viewsets.GenericViewSet):
    def list(self, *args, **kwargs):
        employee = self.request.user
        queryset = Task.objects.filter(employee=employee.id)
        serializer = TaskListSerializer(queryset, many=True)
        if not User.objects.filter(id=employee.id).first():
            return Response({"detail": "Employee does not exist"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def retrieve(self, request, *args, **kwargs):
        try:
            task = Task.objects.get(pk=kwargs.get('pk'))
        except Task.DoesNotExist:
            return Response({"detail": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskRetrieveSerializer(task, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    @action(methods=['post'], detail=True, url_path='start_task')
    def start_task(self, *args, **kwargs):
        employee = self.request.user
        task_id = kwargs.get('pk')
        task = Task.objects.filter(id=task_id, employee=employee.pk).first()
        if not User.objects.filter(id=employee.id).first():
            return Response({"detail": "Employee does not exist"}, status=status.HTTP_401_UNAUTHORIZED)
        if not task:
            return Response({"detail": "Task with this id does not exist"}, status=status.HTTP_404_NOT_FOUND)
        if task.status == "deactive":
            task.start_task()
            return Response({"message": f"Task {task_id} started"}, status=status.HTTP_200_OK)
        if task.status == "active":
            return Response({"detail": f"Task {task_id} already started"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": f"Task {task_id} cannot be started"}, status=status.HTTP_400_BAD_REQUEST)
    
    
    @action(methods=['post'], detail=True, url_path='end_task')
    def end_task(self, *args, **kwargs):
        employee = self.request.user
        task_id = kwargs.get('pk')
        task = Task.objects.filter(id=task_id, employee=employee.pk).first()
        if not User.objects.filter(id=employee.id).first():
            return Response({"detail": "Employee does not exist"}, status=status.HTTP_401_UNAUTHORIZED)
        if not task:
            return Response({"detail": "Task with this id does not exist"}, status=status.HTTP_404_NOT_FOUND)
        if task.status == "active":
            task.end_task()
            return Response({"message": f"Task {task_id} ended"}, status=status.HTTP_200_OK)
        return Response({"detail": f"Task {task_id} cannot be ended"})


    @action(methods=['post'], detail=True, url_path='decline_task')
    def decline_task(self, *args, **kwargs):
        employee = self.request.user
        task_id = kwargs.get('pk')
        task = Task.objects.filter(id=task_id, employee=employee.pk).first()
        if not User.objects.filter(id=employee.id).first():
            return Response({"detail": "Employee does not exist"}, status=status.HTTP_401_UNAUTHORIZED)
        if not task:
            return Response({"detail": "Task with this id does not exist"}, status=status.HTTP_404_NOT_FOUND)
        if task.status == "active":
            task.decline_task()
            return Response({"message": f"Task {task_id} declined"}, status=status.HTTP_200_OK)
        return Response({"detail": f"Task {task_id} cannot be declined"})


    @action(methods=['post'], detail=True, url_path='fail_task')
    def fail_task(self, *args, **kwargs):
        employee = self.request.user
        task_id = kwargs.get('pk')
        task = Task.objects.filter(id=task_id, employee=employee.pk).first()
        if not User.objects.filter(id=employee.id).first():
            return Response({"detail": "Employee does not exist"}, status=status.HTTP_401_UNAUTHORIZED)
        if not task:
            return Response({"detail": "Task with this id does not exist"}, status=status.HTTP_404_NOT_FOUND)
        if task.status == "active":
            task.fail_task()
            return Response({"message": f"Task {task_id} failed"}, status=status.HTTP_200_OK)
        return Response({"detail": f"Task {task_id} cannot be failed"})


    @action(methods=['post'], detail=True, url_path='ask')
    def ask(self, *args, **kwargs):
        employee = self.request.user
        task_id = kwargs.get('pk')
        data = self.request.data
        question = data.get("question")
        task = Task.objects.filter(id=task_id, employee=employee.pk).first()
        if not User.objects.filter(id=employee.id).first():
            return Response({"detail": "Employee does not exist"}, status=status.HTTP_401_UNAUTHORIZED)
        if not task:
            return Response({"detail": "Task with this id does not exist"}, status=status.HTTP_404_NOT_FOUND)
        if task.status != "active":
            return Response({"message": f"Task {task_id} must be started"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            answer="answer"
            Question.objects.create(question=question, answer=answer, task=task)
            return Response({"question": question, "answer": answer}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": f"Something went wrong, please try again{e}"}, status=status.HTTP_400_BAD_REQUEST)
        
