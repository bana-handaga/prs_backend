from django.core.management.base import BaseCommand
from apps.accounts.models import User, Department
from apps.attendance.models import WorkSchedule, StaffSchedule, Holiday
from apps.leave.models import LeaveType
from datetime import time, date


class Command(BaseCommand):
    help = 'Seed data awal untuk sistem presensi DSTI'

    def handle(self, *args, **options):
        self.stdout.write('Membuat departemen...')
        depts = [
            ('IT', 'Teknologi Informasi', 'Departemen IT'),
            ('HR', 'Human Resources', 'Departemen SDM'),
            ('FIN', 'Keuangan', 'Departemen Keuangan'),
            ('OPS', 'Operasional', 'Departemen Operasional'),
            ('MKT', 'Marketing', 'Departemen Marketing'),
        ]
        dept_objs = {}
        for code, name, desc in depts:
            dept, _ = Department.objects.get_or_create(code=code, defaults={'name': name, 'description': desc})
            dept_objs[code] = dept
            self.stdout.write(f'  - {dept}')

        self.stdout.write('Membuat jadwal kerja...')
        schedules = [
            {
                'name': 'Shift Pagi (07:30-16:30)',
                'check_in_start': time(7, 0),
                'check_in_end': time(7, 30),
                'check_out_start': time(16, 0),
                'check_out_end': time(17, 0),
                'late_tolerance': 15,
            },
            {
                'name': 'Shift Normal (08:00-17:00)',
                'check_in_start': time(7, 30),
                'check_in_end': time(8, 0),
                'check_out_start': time(16, 30),
                'check_out_end': time(17, 30),
                'late_tolerance': 15,
            },
            {
                'name': 'WFH (Fleksibel)',
                'check_in_start': time(7, 0),
                'check_in_end': time(9, 0),
                'check_out_start': time(15, 0),
                'check_out_end': time(18, 0),
                'late_tolerance': 60,
            },
        ]
        schedule_objs = {}
        for s in schedules:
            sched, _ = WorkSchedule.objects.get_or_create(name=s['name'], defaults=s)
            schedule_objs[s['name']] = sched
            self.stdout.write(f'  - {sched}')

        self.stdout.write('Membuat jenis cuti...')
        leave_types = [
            ('CT', 'Cuti Tahunan', 12, False),
            ('IS', 'Izin Sakit', None, True),
            ('IP', 'Izin Pribadi', 3, False),
            ('CB', 'Cuti Bersalin', 90, True),
            ('CD', 'Cuti Duka', 3, False),
            ('CL', 'Cuti Lainnya', None, False),
        ]
        for code, name, max_days, req_doc in leave_types:
            lt, _ = LeaveType.objects.get_or_create(
                code=code,
                defaults={'name': name, 'max_days_per_year': max_days, 'requires_document': req_doc}
            )
            self.stdout.write(f'  - {lt}')

        self.stdout.write('Membuat hari libur nasional 2025...')
        holidays_2025 = [
            (date(2025, 1, 1), 'Tahun Baru 2025'),
            (date(2025, 1, 27), 'Isra Miraj'),
            (date(2025, 1, 29), 'Tahun Baru Imlek'),
            (date(2025, 3, 29), 'Hari Raya Nyepi'),
            (date(2025, 3, 31), 'Idul Fitri 1446 H'),
            (date(2025, 4, 1), 'Idul Fitri 1446 H'),
            (date(2025, 4, 18), 'Wafat Isa Almasih'),
            (date(2025, 5, 1), 'Hari Buruh'),
            (date(2025, 5, 12), 'Kenaikan Isa Almasih'),
            (date(2025, 5, 29), 'Hari Raya Waisak'),
            (date(2025, 6, 1), 'Hari Lahir Pancasila'),
            (date(2025, 6, 6), 'Idul Adha 1446 H'),
            (date(2025, 6, 27), 'Tahun Baru Islam 1447 H'),
            (date(2025, 8, 17), 'Hari Kemerdekaan RI'),
            (date(2025, 9, 5), 'Maulid Nabi Muhammad SAW'),
            (date(2025, 12, 25), 'Hari Natal'),
            (date(2025, 12, 26), 'Cuti Bersama Natal'),
        ]
        for hdate, hname in holidays_2025:
            Holiday.objects.get_or_create(date=hdate, defaults={'name': hname})
        self.stdout.write(f'  - {len(holidays_2025)} hari libur dibuat')

        self.stdout.write('Membuat akun admin...')
        if not User.objects.filter(email='admin@dsti.id').exists():
            admin = User.objects.create_superuser(
                email='admin@dsti.id',
                employee_id='ADMIN001',
                full_name='Administrator DSTI',
                password='Admin@dsti2025',
                role=User.Role.ADMIN,
                is_staff=True,
            )
            self.stdout.write(f'  - Admin: {admin.email} / Admin@dsti2025')
        else:
            self.stdout.write('  - Admin sudah ada')

        self.stdout.write(self.style.SUCCESS('\nSeed data selesai!'))
        self.stdout.write(self.style.WARNING(
            '\nLogin admin: admin@dsti.id / Admin@dsti2025'
        ))
        self.stdout.write(self.style.WARNING(
            'PENTING: Ganti password admin setelah login pertama!'
        ))
