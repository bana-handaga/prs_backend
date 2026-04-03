from django.db import models
from django.conf import settings


class WorkSchedule(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nama Jadwal')
    check_in_start = models.TimeField(verbose_name='Mulai Check-in')
    check_in_end = models.TimeField(verbose_name='Batas Check-in (tepat waktu)')
    check_out_start = models.TimeField(verbose_name='Mulai Check-out')
    check_out_end = models.TimeField(verbose_name='Batas Check-out')
    late_tolerance = models.PositiveIntegerField(default=15, verbose_name='Toleransi Terlambat (menit)')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Jadwal Kerja'
        verbose_name_plural = 'Jadwal Kerja'

    def __str__(self):
        return self.name


class StaffSchedule(models.Model):
    class DayOfWeek(models.IntegerChoices):
        MONDAY = 0, 'Senin'
        TUESDAY = 1, 'Selasa'
        WEDNESDAY = 2, 'Rabu'
        THURSDAY = 3, 'Kamis'
        FRIDAY = 4, 'Jumat'
        SATURDAY = 5, 'Sabtu'
        SUNDAY = 6, 'Minggu'

    staff = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='schedules', verbose_name='Staff'
    )
    schedule = models.ForeignKey(
        WorkSchedule, on_delete=models.CASCADE, verbose_name='Jadwal'
    )
    effective_date = models.DateField(null=True, blank=True, verbose_name='Tanggal Tertentu')
    day_of_week = models.IntegerField(
        choices=DayOfWeek.choices, null=True, blank=True, verbose_name='Hari (berulang)'
    )
    is_recurring = models.BooleanField(default=False, verbose_name='Berulang')
    note = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Jadwal Staff'
        verbose_name_plural = 'Jadwal Staff'

    def __str__(self):
        if self.is_recurring:
            return f'{self.staff} - {self.get_day_of_week_display()} - {self.schedule}'
        return f'{self.staff} - {self.effective_date} - {self.schedule}'


class Holiday(models.Model):
    date = models.DateField(unique=True, verbose_name='Tanggal')
    name = models.CharField(max_length=100, verbose_name='Nama Hari Libur')
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['date']
        verbose_name = 'Hari Libur'
        verbose_name_plural = 'Hari Libur'

    def __str__(self):
        return f'{self.date} - {self.name}'


class AttendanceRecord(models.Model):
    class Status(models.TextChoices):
        PRESENT = 'hadir', 'Hadir'
        LATE = 'terlambat', 'Terlambat'
        EARLY_LEAVE = 'pulang_awal', 'Pulang Awal'
        ABSENT = 'absen', 'Absen'
        LEAVE = 'izin', 'Izin/Cuti'
        HOLIDAY = 'libur', 'Hari Libur'
        WFH = 'wfh', 'WFH'

    staff = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        related_name='attendance_records', verbose_name='Staff'
    )
    date = models.DateField(verbose_name='Tanggal')
    schedule = models.ForeignKey(
        WorkSchedule, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Jadwal'
    )

    check_in_time = models.DateTimeField(null=True, blank=True, verbose_name='Waktu Check-in')
    check_in_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    check_in_lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    check_in_photo = models.ImageField(upload_to='selfies/%Y/%m/', null=True, blank=True, verbose_name='Foto Check-in')
    check_in_address = models.CharField(max_length=255, blank=True, null=True, verbose_name='Alamat Check-in')

    check_out_time = models.DateTimeField(null=True, blank=True, verbose_name='Waktu Check-out')
    check_out_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    check_out_lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    check_out_photo = models.ImageField(upload_to='selfies/%Y/%m/', null=True, blank=True, verbose_name='Foto Check-out')

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PRESENT, verbose_name='Status'
    )
    work_duration = models.DurationField(null=True, blank=True, verbose_name='Durasi Kerja')
    is_overtime = models.BooleanField(default=False, verbose_name='Lembur')
    notes = models.TextField(blank=True, null=True, verbose_name='Catatan')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('staff', 'date')
        ordering = ['-date']
        verbose_name = 'Rekap Presensi'
        verbose_name_plural = 'Rekap Presensi'

    def __str__(self):
        return f'{self.staff} - {self.date} - {self.get_status_display()}'

    @property
    def work_duration_hours(self):
        if self.work_duration:
            total_seconds = int(self.work_duration.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            return f'{hours}j {minutes}m'
        return None
