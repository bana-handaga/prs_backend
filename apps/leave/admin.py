from django.contrib import admin
from .models import LeaveType, LeaveRequest


@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'max_days_per_year', 'requires_document', 'is_active']
    list_filter = ['is_active', 'requires_document']


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ['staff', 'leave_type', 'start_date', 'end_date', 'total_days', 'status', 'created_at']
    list_filter = ['status', 'leave_type']
    search_fields = ['staff__full_name', 'staff__employee_id']
    date_hierarchy = 'created_at'
    readonly_fields = ['total_days', 'created_at', 'updated_at']
