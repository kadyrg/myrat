from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Clock
from .serializers import ClockListSerializer, ClockRetrieveSerializer


class ClockViewSet(viewsets.GenericViewSet):
    def list(self, *args, **kwargs):
        employee = self.request.user
        queryset = Clock.objects.filter(employee=employee.pk)
        serializer = ClockListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        try:
            task = Clock.objects.get(pk=kwargs.get('pk'))
        except Clock.DoesNotExist:
            return Response({"detail": "Clock not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ClockRetrieveSerializer(task, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='start_clock')
    def start_clock(self, *args, **kwargs):
        employee = self.request.user
        active_clock = Clock.objects.filter(employee=employee.pk, status="started").first()
        
        if active_clock:
            return Response({"detail": "You have already started clock"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            Clock.objects.create(employee=employee).start_clock()
            return Response({"message": "Clock started successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": "Something went wrong", "error": f"{e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @action(methods=['post'], detail=False, url_path='stop_clock')
    def stop_clock(self, *args, **kwargs):
        employee = self.request.user
        active_clock = Clock.objects.filter(employee=employee.pk, status="started").first()
        
        if not active_clock:
            return Response({"detail": "You don't have active clock"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            active_clock.stop_clock()
            return Response({"message": "Clock stopped successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": "Something went wrong", "error": f"{e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
