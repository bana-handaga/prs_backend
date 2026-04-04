# 3. Panduan Administrator

Administrator memiliki akses penuh ke seluruh fitur sistem.

---

## 3.1 Login

1. Buka https://checkin.dsti-ums.id
2. Klik **"Masuk ke Sistem"**
3. Masukkan email dan password admin
4. Klik **Login**

---

## 3.2 Manajemen Departemen

**Menu:** Sidebar → Departemen

### Tambah Departemen
1. Klik tombol **+ Tambah Departemen**
2. Isi nama departemen
3. Klik **Simpan**

### Edit / Hapus
- Klik ikon **edit** atau **hapus** pada baris departemen

---

## 3.3 Manajemen Staff

**Menu:** Sidebar → Staff

### Tambah Staff Baru
1. Klik **+ Tambah Staff**
2. Isi data:
   - **Employee ID** — kode unik karyawan (contoh: `DST001`)
   - **Nama Lengkap**
   - **Email** — digunakan untuk login
   - **Password** — minimal 8 karakter
   - **Departemen** — pilih dari daftar
   - **Peran** — Staff / Supervisor / Admin
3. Klik **Simpan**

### Edit Staff
1. Klik ikon edit pada baris staff
2. Ubah data yang diperlukan
3. Klik **Simpan**

### Reset Password Staff
1. Klik ikon edit pada staff
2. Isi field **Password Baru**
3. Klik **Simpan**

### Nonaktifkan Staff
1. Klik ikon edit pada staff
2. Nonaktifkan toggle **Aktif**
3. Staff tidak bisa login

---

## 3.4 Manajemen Jadwal Kerja

**Menu:** Sidebar → Jadwal Kerja

### Buat Jadwal Baru
1. Klik **+ Tambah Jadwal**
2. Isi data:
   - **Nama Jadwal** — contoh: `Reguler`, `Shift Pagi`
   - **Jam Masuk** — waktu mulai check-in (contoh: `07:30`)
   - **Batas Masuk** — batas check-in normal (contoh: `08:00`)
   - **Jam Pulang** — waktu mulai bisa check-out (contoh: `16:00`)
   - **Toleransi Terlambat** — menit toleransi keterlambatan (contoh: `15`)
3. Klik **Simpan**

### Assign Jadwal ke Staff
1. Klik **+ Assign Jadwal**
2. Pilih **Staff**
3. Pilih **Jadwal**
4. Pilih mode:
   - **Berulang (Mingguan)** — pilih hari (Senin-Minggu)
   - **Tanggal Tertentu** — pilih tanggal spesifik
5. Klik **Simpan**

> **Catatan:** Staff tanpa jadwal tetap bisa check-in dengan status **Hadir**.

---

## 3.5 Manajemen Hari Libur

**Menu:** Sidebar → Hari Libur

### Tambah Hari Libur
1. Klik **+ Tambah Hari Libur**
2. Isi **Tanggal** dan **Keterangan** (contoh: `Hari Raya Idul Fitri`)
3. Klik **Simpan**

> Staff tidak bisa check-in pada hari yang ditandai sebagai libur.

---

## 3.6 Laporan Kehadiran

**Menu:** Sidebar → Laporan → Kehadiran

### Generate Laporan
1. Pilih **Bulan** dan **Tahun**
2. Pilih **Departemen** (opsional, kosongkan untuk semua)
3. Klik **Tampilkan**
4. Untuk ekspor ke Excel: klik **Download Excel**

### Kolom Laporan
| Kolom | Keterangan |
|-------|-----------|
| Nama | Nama staff |
| Departemen | Departemen staff |
| Hadir | Jumlah hari hadir tepat waktu |
| Terlambat | Jumlah hari terlambat |
| Pulang Awal | Jumlah hari pulang lebih awal |
| Absen | Jumlah hari tidak hadir |
| Izin/Cuti | Jumlah hari cuti disetujui |
| Total Jam | Total jam kerja bulan tersebut |

---

## 3.7 Laporan Cuti

**Menu:** Sidebar → Laporan → Cuti

1. Pilih **Bulan** dan **Tahun**
2. Klik **Tampilkan**
3. Klik **Download Excel** untuk ekspor

---

## 3.8 Rekap Departemen

**Menu:** Sidebar → Laporan → Rekap Departemen

Menampilkan ringkasan kehadiran per departemen dalam satu bulan.

---

## 3.9 Persetujuan Cuti

**Menu:** Sidebar → Persetujuan Cuti

1. Lihat daftar pengajuan cuti yang masuk
2. Klik **Setujui** atau **Tolak**
3. Isi catatan jika perlu (opsional)
4. Konfirmasi aksi

> Admin bisa menyetujui/menolak cuti semua staff. Supervisor hanya bisa untuk staff di departemennya.

---

## 3.10 Koreksi Data Presensi

**Menu:** Django Admin → https://checkin.dsti-ums.id/api/admin/

Untuk koreksi data yang tidak bisa dilakukan dari frontend:

1. Login ke Django Admin
2. Pilih **Attendance Records**
3. Cari record yang perlu dikoreksi
4. Edit status, jam masuk/keluar, atau keterangan
5. Klik **Save**
