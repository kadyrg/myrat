from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User


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


admin.site.register(User, UserAdmin)


admin.site.unregister(Group)
