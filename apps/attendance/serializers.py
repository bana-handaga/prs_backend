from rest_framework import serializers
from .models import WorkSchedule, StaffSchedule, AttendanceRecord, Holiday


class WorkScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSchedule
        fields = '__all__'
        read_only_fields = ['created_at']


class StaffScheduleSerializer(serializers.ModelSerializer):
    staff_name = serializers.CharField(source='staff.full_name', read_only=True)
    schedule_name = serializers.CharField(source='schedule.name', read_only=True)
    day_name = serializers.CharField(source='get_day_of_week_display', read_only=True)

    class Meta:
        model = StaffSchedule
        fields = '__all__'
        read_only_fields = ['created_at']


class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = '__all__'


class AttendanceRecordSerializer(serializers.ModelSerializer):
    staff_name = serializers.CharField(source='staff.full_name', read_only=True)
    staff_employee_id = serializers.CharField(source='staff.employee_id', read_only=True)
    department_name = serializers.SerializerMethodField()
    schedule_name = serializers.SerializerMethodField()

    def get_department_name(self, obj):
        return obj.staff.department.name if obj.staff.department else None

    def get_schedule_name(self, obj):
        return obj.schedule.name if obj.schedule else None
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    work_duration_hours = serializers.CharField(read_only=True)

    class Meta:
        model = AttendanceRecord
        fields = [
            'id', 'staff', 'staff_name', 'staff_employee_id', 'department_name',
            'date', 'schedule', 'schedule_name',
            'check_in_time', 'check_in_lat', 'check_in_lon', 'check_in_photo', 'check_in_address',
            'check_out_time', 'check_out_lat', 'check_out_lon', 'check_out_photo',
            'status', 'status_display', 'work_duration', 'work_duration_hours',
            'is_overtime', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'staff', 'date', 'schedule', 'check_in_time', 'check_out_time',
            'status', 'work_duration', 'created_at', 'updated_at'
        ]


class CheckInSerializer(serializers.Serializer):
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False, allow_null=True)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False, allow_null=True)
    photo = serializers.ImageField(required=False, allow_null=True)
    address = serializers.CharField(max_length=255, required=False, allow_blank=True)
    notes = serializers.CharField(required=False, allow_blank=True)


class CheckOutSerializer(serializers.Serializer):
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False, allow_null=True)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False, allow_null=True)
    photo = serializers.ImageField(required=False, allow_null=True)
    notes = serializers.CharField(required=False, allow_blank=True)


class AttendanceAdminUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceRecord
        fields = ['status', 'notes', 'is_overtime']


class AttendanceSummarySerializer(serializers.Serializer):
    month = serializers.CharField()
    total_working_days = serializers.IntegerField()
    hadir = serializers.IntegerField()
    terlambat = serializers.IntegerField()
    pulang_awal = serializers.IntegerField()
    absen = serializers.IntegerField()
    izin = serializers.IntegerField()
    libur = serializers.IntegerField()
    wfh = serializers.IntegerField()
    total_work_duration = serializers.CharField()
