from django.contrib import admin

from .models import DailyRecord, YearlyRecord, MonthlyRecord
from clocks.models import Clock


class ClockInline(admin.TabularInline):
    model = Clock
    readonly_fields = ("employee", "started_date", "ended_date", "duration", "amount", "status", 'daily_record')
    extra = 0

class DailyRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'month', 'month__year', 'employee', 'amount')
    fieldsets = (
        ('Info', {'fields': ('title', 'employee', 'month', 'amount')}),
    )
    readonly_fields = ('title', 'month', 'employee', 'amount')
    inlines = (ClockInline, )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_view_permission(self, request, obj=None):
        return True
    
admin.site.register(DailyRecord, DailyRecordAdmin)


class DailyRecordInline(admin.TabularInline):
    model = DailyRecord
    readonly_fields = ('title', 'amount')
    extra = 0

class MonthlyRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'year', 'employee', 'amount')
    fieldsets = (
        ('Info', {'fields': ('title', 'employee', 'year', 'amount')}),
    )
    readonly_fields = ('title', 'employee', 'year', 'amount')
    inlines = (DailyRecordInline, )
    
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_view_permission(self, request, obj=None):
        return True
    
admin.site.register(MonthlyRecord, MonthlyRecordAdmin)


class MonthlyRecordInline(admin.TabularInline):
    model = MonthlyRecord
    readonly_fields = ('title', 'amount')
    extra = 0


class YearlyRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'employee', 'amount')
    fieldsets = (
        ('Info', {'fields': ('title', 'employee', 'amount')}),
    )
    readonly_fields = ('title', 'employee', 'amount')
    inlines = (MonthlyRecordInline, )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_view_permission(self, request, obj=None):
        return True
    
admin.site.register(YearlyRecord, YearlyRecordAdmin)
