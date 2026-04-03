from django.db import models
from django.conf import settings


class LeaveType(models.Model):
    name = models.CharField(max_length=100, verbose_name='Jenis Izin/Cuti')
    code = models.CharField(max_length=20, unique=True, verbose_name='Kode')
    max_days_per_year = models.PositiveIntegerField(null=True, blank=True, verbose_name='Maks. Hari/Tahun')
    requires_document = models.BooleanField(default=False, verbose_name='Wajib Lampiran')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Jenis Cuti'
        verbose_name_plural = 'Jenis Cuti'

    def __str__(self):
        return self.name


class LeaveRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'menunggu', 'Menunggu'
        APPROVED = 'disetujui', 'Disetujui'
        REJECTED = 'ditolak', 'Ditolak'
        CANCELLED = 'dibatalkan', 'Dibatalkan'

    staff = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        related_name='leave_requests', verbose_name='Staff'
    )
    leave_type = models.ForeignKey(
        LeaveType, on_delete=models.PROTECT, verbose_name='Jenis Cuti'
    )
    start_date = models.DateField(verbose_name='Tanggal Mulai')
    end_date = models.DateField(verbose_name='Tanggal Selesai')
    total_days = models.PositiveIntegerField(default=0, verbose_name='Total Hari')
    reason = models.TextField(verbose_name='Alasan')
    attachment = models.FileField(
        upload_to='leave_docs/%Y/%m/', null=True, blank=True, verbose_name='Lampiran'
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING, verbose_name='Status'
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='reviewed_leaves', verbose_name='Disetujui Oleh'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True, verbose_name='Waktu Review')
    review_note = models.TextField(blank=True, null=True, verbose_name='Catatan Review')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Permohonan Cuti/Izin'
        verbose_name_plural = 'Permohonan Cuti/Izin'

    def __str__(self):
        return f'{self.staff} - {self.leave_type} ({self.start_date} s/d {self.end_date})'

    def calculate_total_days(self):
        """Count working days (excluding weekends and holidays)."""
        from apps.attendance.models import Holiday
        from datetime import timedelta

        total = 0
        current = self.start_date
        holidays = set(
            Holiday.objects.filter(
                date__gte=self.start_date, date__lte=self.end_date
            ).values_list('date', flat=True)
        )
        while current <= self.end_date:
            if current.weekday() < 5 and current not in holidays:
                total += 1
            current += timedelta(days=1)
        return total
