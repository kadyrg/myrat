from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Task(models.Model):
    class Status(models.TextChoices):
        DEACTIVE = "deactive", "Deactive"
        ACTIVE = "active", "Active"
        DECLINED = "declined", "Declined"
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"
        
    title = models.CharField(max_length=250)
    description = models.TextField()
    employee = models.ForeignKey("accounts.User", verbose_name="Employee", on_delete=models.CASCADE)
    created_date = models.DateTimeField(null=True, blank=True, editable=False)
    started_date = models.DateTimeField(null=True, blank=True, editable=False)
    ended_date = models.DateTimeField(null=True, blank=True, editable=False)
    status = models.CharField(choices=Status, max_length=50, default=Status.DEACTIVE)
    duration = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Duration in hours", null=True, editable=False)
    
    def __str__(self):
        return self.title

    def clean(self):
        if self.employee.type == "manager":
            raise ValidationError("Selected employee has type manager")
        # if self.status in ["success", "failed"]:
        #     instance = Task.objects.get(pk=self.pk)
        #     if instance.status != "active":
        #         raise ValidationError("Only active tasks can be succeed or failed")
        # if self.status == "declined":
        #     instance = Task.objects.get(pk=self.pk)
        #     if instance.status != "deactive":
        #         raise ValidationError("Only deactive tasks can be declined")
            
    def start_task(self, *args, **kwargs):
        self.status = "active"
        self.started_date = timezone.now()
        self.ended_date = None
        self.duration = None
        super().save(*args, **kwargs)

    def end_task(self, *args, **kwargs):
        self.ended_date = timezone.now()
        self.status = "success"
        delta = self.ended_date - self.started_date
        self.duration = round(delta.total_seconds() / 3600, 2)
        super().save(*args, **kwargs)

    def decline_task(self, *args, **kwargs):
        self.started_date = None
        self.ended_date = None
        self.status = "declined"
        self.duration = 0
        super().save(*args, **kwargs)
        
    def fail_task(self, *args, **kwargs):
        self.ended_date = timezone.now()
        self.status = "failed"
        self.duration = 0
        super().save(*args, **kwargs)

    def deactivate_task(self, *args, **kwargs):
        self.created_date = None
        self.started_date = None
        self.ended_date = None
        self.duration = None
        super().save(*args, **kwargs)
        
    def save(self, *args, **kwargs):
        if self.status == "active":
            self.start_task()
        if self.status == "success":
            self.end_task()
        if self.status == "declined":
            self.decline_task()
        if self.status == "failed":
            self.fail_task()
        if self.status == "deactive":
            self.deactivate_task()


class Question(models.Model):
    question = models.CharField(max_length=250, editable=False)
    task = models.ForeignKey("tasks.Task", verbose_name="Task of the question", on_delete=models.CASCADE, editable=False)
    answer = models.TextField(editable=False)
    
    def __str__(self):
        return self.question
