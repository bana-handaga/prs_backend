# Manual Operasi Sistem Presensi Online DSTI

**Sistem:** DSTI Online Presensi  
**Versi:** 1.0.0  
**Instansi:** Direktorat Sistem dan Teknologi Informasi, Universitas Muhammadiyah Surakarta  
**URL Produksi:** https://checkin.dsti-ums.id

---

## Daftar Isi

1. [Pendahuluan](01-pendahuluan.md)
2. [Instalasi & Konfigurasi Server](02-instalasi.md)
3. [Panduan Administrator](03-admin.md)
4. [Panduan Supervisor](04-supervisor.md)
5. [Panduan Staff](05-staff.md)
6. [Troubleshooting](06-troubleshooting.md)

---

## 1. Pendahuluan

### 1.1 Gambaran Umum

Sistem Presensi Online DSTI adalah aplikasi manajemen kehadiran berbasis web yang memungkinkan staff DSTI untuk melakukan presensi secara digital dengan verifikasi lokasi GPS dan foto selfie.

### 1.2 Fitur Utama

| Fitur | Deskripsi |
|-------|-----------|
| Check-in / Check-out | Presensi harian dengan GPS dan foto selfie |
| Manajemen Cuti | Pengajuan dan persetujuan cuti online |
| Jadwal Kerja | Konfigurasi jadwal kerja fleksibel per staff |
| Laporan | Ekspor laporan kehadiran dan cuti ke Excel |
| Multi-role | Admin, Supervisor, dan Staff dengan hak akses berbeda |

### 1.3 Peran Pengguna

| Peran | Deskripsi | Hak Akses |
|-------|-----------|-----------|
| **Admin** | Administrator sistem | Kelola semua data, laporan, jadwal, hari libur |
| **Supervisor** | Kepala unit/divisi | Setujui/tolak cuti, lihat laporan divisi |
| **Staff** | Karyawan biasa | Check-in/out, ajukan cuti, lihat riwayat sendiri |

### 1.4 Teknologi

- **Backend:** Django 4.2 + Django REST Framework
- **Autentikasi:** JWT (JSON Web Token)
- **Database:** MySQL (produksi) / SQLite (pengembangan)
- **File Storage:** Local filesystem
- **Web Server:** LiteSpeed (produksi)

### 1.5 Akun Default

> ⚠️ **Ganti password setelah pertama kali login!**

| Email | Password Default | Peran |
|-------|-----------------|-------|
| admin@dsti.id | Admin@dsti2025 | Admin |
