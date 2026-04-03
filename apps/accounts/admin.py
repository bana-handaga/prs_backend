from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'created_at']
    search_fields = ['name', 'code']


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['employee_id', 'full_name', 'email', 'department', 'role', 'is_active']
    list_filter = ['role', 'department', 'is_active']
    search_fields = ['employee_id', 'full_name', 'email']
    ordering = ['full_name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Info Pribadi', {'fields': ('employee_id', 'full_name', 'phone', 'photo_profile')}),
        ('Organisasi', {'fields': ('department', 'role')}),
        ('Hak Akses', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Tanggal', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'employee_id', 'full_name', 'role', 'department', 'password1', 'password2'),
        }),
    )
    readonly_fields = ['date_joined', 'last_login']
