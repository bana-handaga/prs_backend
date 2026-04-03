from datetime import timedelta
from django.utils import timezone
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.accounts.permissions import IsAdmin, IsAdminOrSupervisor
from .models import WorkSchedule, StaffSchedule, AttendanceRecord, Holiday
from .serializers import (
    WorkScheduleSerializer, StaffScheduleSerializer,
    AttendanceRecordSerializer, CheckInSerializer, CheckOutSerializer,
    AttendanceAdminUpdateSerializer, HolidaySerializer
)
from .filters import AttendanceFilter
from .utils import (
    get_jakarta_now, get_staff_schedule_for_date,
    compute_attendance_status, compute_checkout_status
)


class CheckInView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CheckInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        now = timezone.now()
        today = now.astimezone(timezone.get_current_timezone()).date()
        user = request.user

        # Check for approved leave today
        approved_leave = user.leave_requests.filter(
            start_date__lte=today,
            end_date__gte=today,
            status='disetujui'
        ).exists()
        if approved_leave:
            return Response(
                {'detail': 'Anda memiliki izin/cuti yang telah disetujui untuk hari ini.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check for holiday
        is_holiday = Holiday.objects.filter(date=today).exists()
        if is_holiday:
            return Response(
                {'detail': 'Hari ini adalah hari libur.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get or create today's record
        record, created = AttendanceRecord.objects.get_or_create(
            staff=user, date=today,
            defaults={'schedule': get_staff_schedule_for_date(user, today)}
        )

        if record.check_in_time:
            return Response(
                {'detail': 'Anda sudah melakukan check-in hari ini.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data
        record.check_in_time = now
        record.check_in_lat = data.get('latitude')
        record.check_in_lon = data.get('longitude')
        record.check_in_address = data.get('address', '')
        if data.get('photo'):
            record.check_in_photo = data['photo']
        if data.get('notes'):
            record.notes = data['notes']

        # Compute status
        att_status, _ = compute_attendance_status(now, record.schedule)
        record.status = att_status
        record.save()

        return Response(AttendanceRecordSerializer(record).data, status=status.HTTP_200_OK)


class CheckOutView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CheckOutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        now = timezone.now()
        today = now.astimezone(timezone.get_current_timezone()).date()
        user = request.user

        try:
            record = AttendanceRecord.objects.get(staff=user, date=today)
        except AttendanceRecord.DoesNotExist:
            return Response(
                {'detail': 'Anda belum melakukan check-in hari ini.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not record.check_in_time:
            return Response(
                {'detail': 'Anda belum melakukan check-in hari ini.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if record.check_out_time:
            return Response(
                {'detail': 'Anda sudah melakukan check-out hari ini.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data
        record.check_out_time = now
        record.check_out_lat = data.get('latitude')
        record.check_out_lon = data.get('longitude')
        if data.get('photo'):
            record.check_out_photo = data['photo']
        if data.get('notes'):
            record.notes = (record.notes or '') + f'\n[Check-out] {data["notes"]}'

        # Work duration
        record.work_duration = now - record.check_in_time

        # Check early leave status
        updated_status = compute_checkout_status(record, now)
        if updated_status != record.status:
            record.status = updated_status

        # Overtime check: if work > scheduled hours + 1h
        if record.schedule and record.work_duration:
            scheduled_end = timezone.make_aware(
                __import__('datetime').datetime.combine(today, record.schedule.check_out_end)
            )
            if record.check_out_time > scheduled_end + timedelta(hours=1):
                record.is_overtime = True

        record.save()
        return Response(AttendanceRecordSerializer(record).data, status=status.HTTP_200_OK)


class TodayAttendanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.now().astimezone(timezone.get_current_timezone()).date()
        try:
            record = AttendanceRecord.objects.select_related('schedule').get(
                staff=request.user, date=today
            )
            return Response(AttendanceRecordSerializer(record).data)
        except AttendanceRecord.DoesNotExist:
            return Response(None)


class AttendanceSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        month_param = request.query_params.get('month')
        if month_param:
            try:
                year, month = month_param.split('-')
                year, month = int(year), int(month)
            except ValueError:
                return Response({'detail': 'Format bulan tidak valid. Gunakan YYYY-MM.'}, status=400)
        else:
            now = timezone.now().astimezone(timezone.get_current_timezone())
            year, month = now.year, now.month

        records = AttendanceRecord.objects.filter(
            staff=request.user, date__year=year, date__month=month
        )

        total_duration = timedelta()
        for r in records:
            if r.work_duration:
                total_duration += r.work_duration

        status_counts = {s: 0 for s in ['hadir', 'terlambat', 'pulang_awal', 'absen', 'izin', 'libur', 'wfh']}
        for r in records:
            if r.status in status_counts:
                status_counts[r.status] += 1

        total_seconds = int(total_duration.total_seconds())
        hours, rem = divmod(total_seconds, 3600)
        minutes, _ = divmod(rem, 60)

        return Response({
            'month': f'{year}-{month:02d}',
            'total_working_days': records.count(),
            **status_counts,
            'total_work_duration': f'{hours}j {minutes}m',
        })


class AttendanceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AttendanceFilter
    search_fields = ['staff__full_name', 'staff__employee_id']
    ordering_fields = ['date', 'check_in_time', 'status']
    ordering = ['-date']

    def get_queryset(self):
        qs = AttendanceRecord.objects.select_related('staff', 'staff__department', 'schedule')
        if self.request.user.role == 'admin' or self.request.user.role == 'supervisor':
            return qs
        return qs.filter(staff=self.request.user)

    def get_serializer_class(self):
        if self.action in ('update', 'partial_update') and self.request.user.role == 'admin':
            return AttendanceAdminUpdateSerializer
        return AttendanceRecordSerializer

    def destroy(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            return Response({'detail': 'Tidak diizinkan.'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


class WorkScheduleViewSet(viewsets.ModelViewSet):
    queryset = WorkSchedule.objects.all()
    serializer_class = WorkScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get'], url_path='my-schedule')
    def my_schedule(self, request):
        from django.utils import timezone as tz
        today = tz.now().astimezone(tz.get_current_timezone()).date()
        schedule = get_staff_schedule_for_date(request.user, today)
        if schedule:
            return Response(WorkScheduleSerializer(schedule).data)
        return Response(None)

    @action(detail=False, methods=['post'], url_path='assign', permission_classes=[IsAuthenticated, IsAdmin])
    def assign(self, request):
        serializer = StaffScheduleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class HolidayViewSet(viewsets.ModelViewSet):
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering = ['date']

    def get_queryset(self):
        qs = super().get_queryset()
        year = self.request.query_params.get('year')
        if year:
            qs = qs.filter(date__year=year)
        return qs

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]
