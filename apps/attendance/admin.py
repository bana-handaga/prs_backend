from django.contrib import admin
from .models import WorkSchedule, StaffSchedule, AttendanceRecord, Holiday


@admin.register(WorkSchedule)
class WorkScheduleAdmin(admin.ModelAdmin):
    list_display = ['name', 'check_in_start', 'check_in_end', 'check_out_start', 'check_out_end', 'late_tolerance', 'is_active']
    list_filter = ['is_active']


@admin.register(StaffSchedule)
class StaffScheduleAdmin(admin.ModelAdmin):
    list_display = ['staff', 'schedule', 'is_recurring', 'day_of_week', 'effective_date']
    list_filter = ['is_recurring', 'schedule']
    search_fields = ['staff__full_name', 'staff__employee_id']


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ['staff', 'date', 'status', 'check_in_time', 'check_out_time', 'work_duration_hours', 'is_overtime']
    list_filter = ['status', 'is_overtime', 'date']
    search_fields = ['staff__full_name', 'staff__employee_id']
    date_hierarchy = 'date'
    readonly_fields = ['work_duration', 'created_at', 'updated_at']


@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ['date', 'name']
    date_hierarchy = 'date'
