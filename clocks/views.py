from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import Clock
from .serializers import ClockListSerializer


class ClockPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    
class ClockViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    pagination_class = ClockPagination
    serializer_class = ClockListSerializer

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


    @action(methods=['get'], detail=False, url_path='last_clock')
    def last_clock(self, *args, **kwargs):
        employee = self.request.user
        last_clock = Clock.objects.filter(employee=employee.pk).last()
        serailizer = ClockListSerializer(last_clock)
        if not employee.is_authenticated:
            return Response({"detail": "You are not authorized"}, status=status.HTTP_401_UNAUTHORIZED)
        if not last_clock:
            return Response({"detail": "You don't have any clocks yet"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serailizer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        employee = self.request.user
        return Clock.objects.filter(employee=employee.pk).order_by('-started_date')
