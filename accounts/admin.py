from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User
from clocks.models import Clock


class ClockInline(admin.TabularInline):
    model = Clock
    extra = 0
    readonly_fields = ("id", "employee", "started_date", "ended_date", "duration", "status")
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "first_name", "last_name")
    list_editable = ("email", "first_name", "last_name")
    list_filter = ('type', )
    fieldsets = (
        ('Info', {'fields': ('email', 'first_name', 'last_name')}),
        ('Details', {'fields': ('type', 'new_password', 'is_active', 'date_joined')}),
    )
    readonly_fields = ('date_joined', 'password')
    search_fields = ('email', 'first_name', 'last_name')
    inlines = [ClockInline]

admin.site.register(User, UserAdmin)


admin.site.unregister(Group)
