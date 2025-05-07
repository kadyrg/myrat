from django.db import models
from django.db.models import Sum
from datetime import date


class YearlyRecord(models.Model):
    title = models.CharField(max_length=50, editable=False)
    amount = models.DecimalField("Total amount in this year", max_digits=15, decimal_places=2, null=True, editable=False)
    employee = models.ForeignKey("accounts.User", verbose_name="Employee of the Record", on_delete=models.CASCADE, editable=False)
    
    def __str__(self):
        return self.title

    def update_total(self, *args, **kwargs):
        self.amount = self.monthly_records.aggregate(total=Sum('amount'))['total'] or 0
        super().save(*args, **kwargs)
    

class MonthlyRecord(models.Model):
    title = models.CharField(max_length=50, editable=False)
    year = models.ForeignKey(YearlyRecord, verbose_name="Year of this day", on_delete=models.CASCADE, related_name="monthly_records")
    amount = models.DecimalField("Total amount in this month", max_digits=15, decimal_places=2, null=True, editable=False)
    employee = models.ForeignKey("accounts.User", verbose_name="Employee of the Record", on_delete=models.CASCADE, editable=False)
    
    def __str__(self):
        return self.title

    def update_total(self, *args, **kwargs):
        self.amount = self.daily_records.aggregate(total=Sum('amount'))['total'] or 0
        super().save(*args, **kwargs)


class DailyRecord(models.Model):
    title = models.CharField(max_length=50, editable=False)
    month = models.ForeignKey(MonthlyRecord, verbose_name="Month of this day", on_delete=models.CASCADE, related_name="daily_records")
    amount = models.DecimalField("Total amount in this day", max_digits=15, decimal_places=2, null=True, editable=False)
    employee = models.ForeignKey("accounts.User", verbose_name="Employee of the Record", on_delete=models.CASCADE, editable=False)
    created_date = models.DateField(editable=False, null=True)
    
    def __str__(self):
        return self.title

    def update_total(self, *args, **kwargs):
        self.amount = self.clocks.aggregate(total=Sum('amount'))['total'] or 0
        super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_date = date.today()
        super().save(*args, **kwargs)
    