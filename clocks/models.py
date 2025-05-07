from django.db import models
from django.utils import timezone
from decimal import Decimal

from records.models import DailyRecord, YearlyRecord, MonthlyRecord


class Clock(models.Model):
    class Status(models.TextChoices):
        STARTED = "started", "Started"
        FINISHED = "finished", "Finished"

    employee = models.ForeignKey("accounts.User", verbose_name="Employee", on_delete=models.CASCADE, editable=False)
    started_date = models.DateTimeField(null=True, blank=True, editable=False)
    ended_date = models.DateTimeField(null=True, blank=True, editable=False)
    duration = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Duration in hours", null=True, editable=False)
    status = models.CharField(choices=Status, max_length=50, default="started", editable=False)
    amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, editable=False)
    daily_record = models.ForeignKey("records.DailyRecord", verbose_name="Daily record of the clock", on_delete=models.CASCADE, related_name="clocks", null=True, editable=False)
    
    def __str__(self):
        return self.employee.email
            
    def start_clock(self, *args, **kwargs):
        self.started_date = timezone.now()
        self.status = "started"
        super().save(*args, **kwargs)
    
    def stop_clock(self, *args, **kwargs):
        self.ended_date = timezone.now()
        delta = self.ended_date - self.started_date
        self.duration = round(delta.total_seconds() / 3600, 2)
        self.amount = Decimal(str(self.duration)) * Decimal(str(self.employee.hourly_salary))
        self.status = "finished"
        year = self.started_date.strftime('%Y')
        month = self.started_date.strftime('%b')
        day = self.started_date.strftime('%a')
        yearly_record, _ = YearlyRecord.objects.get_or_create(
            title = year,
            employee = self.employee
        )
        monthly_record, _ = MonthlyRecord.objects.get_or_create(
            title = month,
            year = yearly_record,
            employee = self.employee
        )
        daily_record, _ = DailyRecord.objects.get_or_create(
            title = day,
            month = monthly_record,
            employee = self.employee
        )
        self.daily_record = daily_record
        super().save(*args, **kwargs)
        daily_record.update_total()
        monthly_record.update_total()
        yearly_record.update_total()
