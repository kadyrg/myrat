from django.contrib import admin

from .models import Clock


class ClockAdmin(admin.ModelAdmin):
    list_display = ("id", "employee", "started_date", "ended_date", "duration", "status")
    
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_view_permission(self, request, obj=None):
        return True
    
admin.site.register(Clock, ClockAdmin)
