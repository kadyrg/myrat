from django.db import models
from django.utils import timezone


class Clock(models.Model):
    class Status(models.TextChoices):
        STARTED = "started", "Started"
        FINISHED = "finished", "Finished"

    employee = models.ForeignKey("accounts.User", verbose_name="Employee", on_delete=models.CASCADE)
    started_date = models.DateTimeField(null=True, blank=True, editable=False)
    ended_date = models.DateTimeField(null=True, blank=True, editable=False)
    duration = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Duration in hours", null=True, editable=False)
    status = models.CharField(choices=Status, max_length=50, default="started", editable=False)
    
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
        self.status = "finished"
        super().save(*args, **kwargs)

