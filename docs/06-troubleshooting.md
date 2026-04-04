# 6. Troubleshooting

---

## 6.1 Masalah Login

### "Email atau password salah"
- Pastikan email dan password benar
- Password bersifat case-sensitive
- Hubungi admin untuk reset password

### Tidak bisa login setelah beberapa saat
- Token mungkin kadaluarsa — refresh halaman dan login ulang
- Coba clear cache browser: `Ctrl + Shift + Delete`

---

## 6.2 Masalah GPS / Lokasi

### "GPS tidak tersedia pada koneksi HTTP"
- **Penyebab:** Browser memblok GPS di koneksi non-HTTPS
- **Solusi:** Akses via `https://checkin.dsti-ums.id` (bukan `http://`)

### "Izin lokasi ditolak"
- **Penyebab:** Browser tidak mendapat izin akses lokasi
- **Solusi:**
  1. Klik ikon gembok 🔒 di address bar browser
  2. Ubah izin **Lokasi** menjadi **Izinkan**
  3. Refresh halaman

### GPS lama muncul atau tidak akurat
- Pastikan GPS HP aktif (Settings → Location → On)
- Pindah ke tempat dengan sinyal GPS lebih baik (dekat jendela)
- Gunakan fitur **Input Manual** jika GPS tidak tersedia

---

## 6.3 Masalah Kamera

### "Tidak dapat mengakses kamera"
- **Penyebab:** Browser tidak mendapat izin kamera
- **Solusi:**
  1. Klik ikon gembok 🔒 di address bar
  2. Ubah izin **Kamera** menjadi **Izinkan**
  3. Refresh halaman dan coba lagi

### Kamera tidak muncul di HP
- Pastikan tidak ada aplikasi lain yang sedang menggunakan kamera
- Coba gunakan Chrome (bukan browser bawaan HP)

---

## 6.4 Masalah Check-in

### "Anda sudah melakukan check-in hari ini"
- Check-in hanya bisa dilakukan sekali per hari
- Jika data check-in salah, hubungi admin untuk koreksi

### "Hari ini adalah hari libur"
- Admin telah menandai hari ini sebagai hari libur nasional
- Hubungi admin jika terjadi kesalahan konfigurasi

### "Anda memiliki izin/cuti yang telah disetujui"
- Anda memiliki cuti yang sudah disetujui untuk hari ini
- Tidak bisa check-in pada hari cuti disetujui

### "Gagal melakukan presensi" (error umum)
- Cek koneksi internet
- Refresh halaman dan coba lagi
- Jika terus terjadi, hubungi admin

---

## 6.5 Masalah Server / Produksi

### Semua endpoint timeout
```bash
# Cek apakah passenger app jalan
ps aux | grep lswsgi | grep -v grep

# Jika tidak ada output, restart app
touch /home/umsbirot/checkin.dsti-ums.id/api/passenger_wsgi.py
```

### Error 500 Internal Server Error
```bash
# Cek Django dapat start
cd /home/umsbirot/checkin.dsti-ums.id/api
python manage.py check --settings=config.settings.production

# Cek koneksi database
python manage.py shell --settings=config.settings.production -c \
  "from django.db import connection; connection.ensure_connection(); print('DB OK')"
```

### Static files (CSS/JS) tidak muncul di admin
```bash
cd /home/umsbirot/checkin.dsti-ums.id/api
python manage.py collectstatic --noinput --settings=config.settings.production
cp -r staticfiles/. ../public_html/static/
```

### Halaman frontend 404 saat refresh
- Pastikan file `.htaccess` ada di `public_html/` dengan isi:
```apache
Options -MultiViews
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^ index.html [L]
```

### "Data autentikasi tidak diberikan" padahal sudah login
- LiteSpeed strip Authorization header
- Pastikan `.htaccess` di folder `api/` berisi:
```apache
RewriteEngine On
RewriteCond %{HTTP:Authorization} .
RewriteRule ^ - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
```
- Pastikan `passenger_wsgi.py` sudah diupdate dengan wrapper restore header

---

## 6.6 Kontak Dukungan

Untuk masalah yang tidak bisa diselesaikan sendiri:

| Jenis Masalah | Hubungi |
|---------------|---------|
| Lupa password | Administrator DSTI |
| Data presensi salah | Administrator DSTI |
| Masalah teknis server | Tim IT DSTI |
| Bug aplikasi | Developer (GitHub Issues) |

**GitHub Repository:** https://github.com/bana-handaga/prs_backend
