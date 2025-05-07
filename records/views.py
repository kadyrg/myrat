from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from datetime import timedelta
from django.utils.timezone import now
from collections import OrderedDict

from .models import DailyRecord
from clocks.models import Clock
from .serializers import DailyRecordSerializer


class PerformanceViewSet(viewsets.GenericViewSet):
    @action(methods=['get'], detail=False, url_path='weekly')
    def weekly(self, *args, **kwargs):
        employee = self.request.user
        
        this_year = timezone.now().strftime('%Y')
        this_month = timezone.now().strftime('%b')
        today = timezone.now().strftime('%a')
        
        today_date = now().date()
        start_of_week = today_date - timedelta(days=today_date.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        weekly_records = DailyRecord.objects.filter(
            created_date__range=(start_of_week, end_of_week),
            employee=employee.pk
        )
        week_data = OrderedDict()
        for i in range(7):
            day = start_of_week + timedelta(days=i)
            week_data[day.strftime("%A")] = {
                "date": day.strftime("%a"),
                "amount": 0
            }
        for record in weekly_records:
            day_name = record.created_date.strftime("%A")
            week_data[day_name]["amount"] = record.amount
        response_data = list(week_data.values())
        highest_amount = max(response_data, key=lambda x: x["amount"])
        total_amount = sum(item["amount"] for item in response_data)
        average_amount = round(total_amount / len(response_data) if response_data else 0)
        return Response({'weekly': response_data,
                         'highest': highest_amount,
                         'average': average_amount})
