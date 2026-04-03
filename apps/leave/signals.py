from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender='leave.LeaveRequest')
def sync_leave_to_attendance(sender, instance, **kwargs):
    """
    When a LeaveRequest is approved, create/update AttendanceRecord for covered dates.
    When cancelled/rejected, revert those records if they haven't been checked in.
    """
    from apps.attendance.models import AttendanceRecord, Holiday

    if instance.status == 'disetujui':
        holidays = set(
            Holiday.objects.filter(
                date__gte=instance.start_date, date__lte=instance.end_date
            ).values_list('date', flat=True)
        )
        current = instance.start_date
        while current <= instance.end_date:
            # Skip weekends and holidays
            if current.weekday() < 5 and current not in holidays:
                AttendanceRecord.objects.update_or_create(
                    staff=instance.staff,
                    date=current,
                    defaults={
                        'status': AttendanceRecord.Status.LEAVE,
                        'schedule': None,
                        'notes': f'Izin: {instance.leave_type.name}',
                    }
                )
            current += timedelta(days=1)

    elif instance.status in ('ditolak', 'dibatalkan'):
        # Remove leave records if staff hasn't actually checked in
        current = instance.start_date
        while current <= instance.end_date:
            AttendanceRecord.objects.filter(
                staff=instance.staff,
                date=current,
                status=AttendanceRecord.Status.LEAVE,
                check_in_time__isnull=True
            ).delete()
            current += timedelta(days=1)
