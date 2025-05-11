from django.contrib import admin

from .models import Task, Question


class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "employee", "status", "created_date", "started_date", "ended_date", "duration")
    list_editable = ("title", "employee", "status")
    fieldsets = (
        ('Info', {'fields': ('title', 'description', 'employee')}),
        ('Details', {'fields': ("status", 'created_date', 'started_date', 'ended_date', "duration")}),
    )
    readonly_fields = ('created_date', 'started_date', 'ended_date', "duration")
    search_fields = ('title', 'employee')


admin.site.register(Task, TaskAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'task', 'answer')
    fieldsets = (
        (None, {"fields": ( 'question', 'task', 'answer')}),
    )
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_view_permission(self, request, obj=None):
        return True
    
admin.site.register(Question, QuestionAdmin)
