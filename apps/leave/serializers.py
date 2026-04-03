from rest_framework import serializers
from django.utils import timezone
from .models import LeaveType, LeaveRequest


class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = '__all__'


class LeaveRequestSerializer(serializers.ModelSerializer):
    staff_name = serializers.CharField(source='staff.full_name', read_only=True)
    staff_employee_id = serializers.CharField(source='staff.employee_id', read_only=True)
    leave_type_name = serializers.CharField(source='leave_type.name', read_only=True)
    reviewed_by_name = serializers.CharField(source='reviewed_by.full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = LeaveRequest
        fields = [
            'id', 'staff', 'staff_name', 'staff_employee_id',
            'leave_type', 'leave_type_name',
            'start_date', 'end_date', 'total_days', 'reason', 'attachment',
            'status', 'status_display',
            'reviewed_by', 'reviewed_by_name', 'reviewed_at', 'review_note',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'staff', 'total_days', 'status', 'reviewed_by',
            'reviewed_at', 'review_note', 'created_at', 'updated_at'
        ]


class LeaveRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = ['leave_type', 'start_date', 'end_date', 'reason', 'attachment']

    def validate(self, attrs):
        if attrs['start_date'] > attrs['end_date']:
            raise serializers.ValidationError('Tanggal mulai tidak boleh setelah tanggal selesai.')
        if attrs['start_date'] < timezone.now().date():
            raise serializers.ValidationError('Tidak dapat mengajukan izin untuk tanggal yang telah lewat.')

        leave_type = attrs['leave_type']
        if leave_type.requires_document and not attrs.get('attachment'):
            raise serializers.ValidationError(
                f'Jenis cuti "{leave_type.name}" memerlukan lampiran dokumen.'
            )
        return attrs

    def create(self, validated_data):
        request = self.context['request']
        instance = LeaveRequest(**validated_data, staff=request.user)
        instance.total_days = instance.calculate_total_days()
        instance.save()
        return instance


class ReviewSerializer(serializers.Serializer):
    review_note = serializers.CharField(required=False, allow_blank=True)


class LeaveBalanceSerializer(serializers.Serializer):
    leave_type_id = serializers.IntegerField()
    leave_type_name = serializers.CharField()
    max_days = serializers.IntegerField(allow_null=True)
    used_days = serializers.IntegerField()
    remaining_days = serializers.IntegerField(allow_null=True)
