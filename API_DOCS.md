# DSTI Online Presensi - API Documentation

Base URL: `http://localhost:8000/api/v1/`

## Authentication
Semua endpoint memerlukan header: `Authorization: Bearer <access_token>`

---

## Auth Endpoints

| Method | Endpoint | Deskripsi | Auth |
|--------|----------|-----------|------|
| POST | `/auth/login/` | Login, mendapatkan JWT token | - |
| POST | `/auth/token/refresh/` | Refresh access token | - |
| POST | `/auth/logout/` | Logout (blacklist refresh token) | ✓ |
| GET/PATCH | `/auth/me/` | Profil sendiri | ✓ |
| POST | `/auth/change-password/` | Ganti password | ✓ |

### Login Request
```json
POST /auth/login/
{
  "email": "admin@dsti.id",
  "password": "Admin@dsti2025"
}
```

---

## Staff Management (Admin only)

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/staff/` | List staff (filter: department, role, is_active) |
| POST | `/staff/` | Tambah staff baru |
| GET | `/staff/{id}/` | Detail staff |
| PATCH | `/staff/{id}/` | Update staff |
| DELETE | `/staff/{id}/` | Nonaktifkan staff |
| POST | `/staff/{id}/reset-password/` | Reset password staff |

---

## Departemen (Admin only)

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/departments/` | List departemen |
| POST | `/departments/` | Tambah departemen |
| PATCH | `/departments/{id}/` | Update departemen |
| DELETE | `/departments/{id}/` | Hapus departemen |

---

## Jadwal Kerja

| Method | Endpoint | Deskripsi | Role |
|--------|----------|-----------|------|
| GET | `/schedules/` | List jadwal | Semua |
| POST | `/schedules/` | Tambah jadwal | Admin |
| PATCH | `/schedules/{id}/` | Update jadwal | Admin |
| GET | `/schedules/my-schedule/` | Jadwal saya hari ini | Semua |
| POST | `/schedules/assign/` | Assign jadwal ke staff | Admin |

---

## Presensi

| Method | Endpoint | Deskripsi | Role |
|--------|----------|-----------|------|
| POST | `/attendance/check-in/` | Check-in (GPS + foto opsional) | Semua |
| POST | `/attendance/check-out/` | Check-out | Semua |
| GET | `/attendance/today/` | Presensi hari ini | Semua |
| GET | `/attendance/summary/` | Rekap bulanan saya | Semua |
| GET | `/attendance/` | List presensi (admin: semua, staff: milik sendiri) | Semua |
| PATCH | `/attendance/{id}/` | Koreksi presensi | Admin |
| DELETE | `/attendance/{id}/` | Hapus record | Admin |

### Check-in Request
```json
POST /attendance/check-in/
Content-Type: multipart/form-data

latitude: -6.2088
longitude: 106.8456
address: "Kantor DSTI Jakarta"
photo: <file>  (opsional)
notes: "WFH dari rumah"  (opsional)
```

### Filter Presensi
```
GET /attendance/?month=2026-04&status=hadir&department=1&staff_id=5
GET /attendance/?date_from=2026-04-01&date_to=2026-04-30
```

---

## Izin & Cuti

| Method | Endpoint | Deskripsi | Role |
|--------|----------|-----------|------|
| GET | `/leave/types/` | List jenis cuti | Semua |
| POST | `/leave/types/` | Tambah jenis cuti | Admin |
| GET | `/leave/requests/` | List permohonan | Semua |
| POST | `/leave/requests/` | Ajukan permohonan | Semua |
| PATCH | `/leave/requests/{id}/` | Batalkan permohonan | Staff (sendiri) |
| POST | `/leave/requests/{id}/approve/` | Setujui permohonan | Admin/Supervisor |
| POST | `/leave/requests/{id}/reject/` | Tolak permohonan | Admin/Supervisor |
| GET | `/leave/balance/` | Sisa kuota cuti | Semua |

---

## Laporan (Admin/Supervisor)

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/reports/attendance/?month=YYYY-MM` | Laporan presensi (JSON) |
| GET | `/reports/attendance/export/?month=YYYY-MM` | Download Excel |
| GET | `/reports/leave/?year=YYYY` | Laporan cuti |
| GET | `/reports/summary/?month=YYYY-MM` | Rekap per departemen |

---

## Hari Libur

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/holidays/?year=2025` | List hari libur | 
| POST | `/holidays/` | Tambah hari libur (Admin) |
| PATCH | `/holidays/{id}/` | Update (Admin) |
| DELETE | `/holidays/{id}/` | Hapus (Admin) |

---

## Status Presensi
- `hadir` - Hadir tepat waktu
- `terlambat` - Terlambat
- `pulang_awal` - Pulang lebih awal
- `absen` - Tidak hadir tanpa keterangan
- `izin` - Izin/Cuti disetujui
- `libur` - Hari libur
- `wfh` - Work From Home

---

## Menjalankan Server

```bash
cd app_backend

# Development (SQLite)
python manage.py runserver

# Dengan MySQL (production)
cp .env.example .env
# Edit .env sesuai konfigurasi
DJANGO_SETTINGS_MODULE=config.settings.production python manage.py runserver
```

## Seed Data Awal
```bash
python manage.py seed_data
```
Admin default: `admin@dsti.id` / `Admin@dsti2025`
