from datetime import datetime, timedelta
import pytz
from django.utils import timezone


def get_jakarta_now():
    jakarta = pytz.timezone('Asia/Jakarta')
    return datetime.now(jakarta)


def compute_attendance_status(check_in_time, schedule):
    """
    Returns (status, is_late) based on check-in time vs schedule.
    check_in_time: aware datetime
    """
    from .models import AttendanceRecord

    if not schedule:
        return AttendanceRecord.Status.PRESENT, False

    jakarta = pytz.timezone('Asia/Jakarta')
    local_check_in = check_in_time.astimezone(jakarta)
    check_in_time_only = local_check_in.time()

    late_cutoff_dt = datetime.combine(local_check_in.date(), schedule.check_in_end)
    late_cutoff_dt += timedelta(minutes=schedule.late_tolerance)
    late_cutoff = late_cutoff_dt.time()

    if check_in_time_only > late_cutoff:
        return AttendanceRecord.Status.LATE, True
    return AttendanceRecord.Status.PRESENT, False


def compute_checkout_status(record, check_out_time):
    """
    Check whether staff is leaving early based on schedule.
    Returns updated status.
    """
    from .models import AttendanceRecord

    if not record.schedule:
        return record.status

    jakarta = pytz.timezone('Asia/Jakarta')
    local_check_out = check_out_time.astimezone(jakarta)
    check_out_time_only = local_check_out.time()

    if check_out_time_only < record.schedule.check_out_start:
        return AttendanceRecord.Status.EARLY_LEAVE
    return record.status


def get_staff_schedule_for_date(staff, date):
    """
    Resolve which WorkSchedule applies for a staff member on a given date.
    Priority: specific date override > recurring weekday > None
    """
    from .models import StaffSchedule

    # 1. Exact date match
    exact = StaffSchedule.objects.filter(
        staff=staff, effective_date=date, is_recurring=False
    ).select_related('schedule').first()
    if exact:
        return exact.schedule

    # 2. Recurring weekday
    weekday = date.weekday()  # 0=Monday
    recurring = StaffSchedule.objects.filter(
        staff=staff, day_of_week=weekday, is_recurring=True
    ).select_related('schedule').first()
    if recurring:
        return recurring.schedule

    return None
