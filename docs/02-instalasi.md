# 2. Instalasi & Konfigurasi Server

## 2.1 Persyaratan Sistem

| Komponen | Minimum |
|----------|---------|
| Python | 3.10+ |
| Database | MySQL 8.0+ / SQLite 3 |
| Web Server | Nginx / Apache / LiteSpeed |
| RAM | 512 MB |
| Storage | 2 GB |

## 2.2 Instalasi Lokal (Development)

### Clone Repository
```bash
git clone https://github.com/bana-handaga/prs_backend.git
cd prs_backend
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Konfigurasi Environment
Buat file `.env` di root project:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:4200,http://127.0.0.1:4200
```

### Migrasi Database
```bash
python manage.py migrate --settings=config.settings.development
```

### Seed Data Awal
```bash
python manage.py seed_data --settings=config.settings.development
```

### Jalankan Server
```bash
python manage.py runserver 0.0.0.0:8000 --settings=config.settings.development
```

---

## 2.3 Instalasi Produksi (LiteSpeed / cPanel)

### Struktur Direktori di Server
```
/home/umsbirot/checkin.dsti-ums.id/
├── api/                    ← project Django
│   ├── apps/
│   ├── config/
│   ├── manage.py
│   ├── requirements.txt
│   ├── passenger_wsgi.py
│   ├── .env
│   └── staticfiles/
└── public_html/            ← frontend Angular + static files
    ├── index.html
    ├── static/             ← Django admin static files
    └── *.js / *.css
```

### File `passenger_wsgi.py`
```python
import sys, os

sys.path.insert(0, "/home/umsbirot/checkin.dsti-ums.id/api")
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.production'

from django.core.wsgi import get_wsgi_application
_application = get_wsgi_application()

def application(environ, start_response):
    # LiteSpeed strips Authorization header — restore dari rewrite rule
    if 'HTTP_AUTHORIZATION' not in environ:
        auth = environ.get('REDIRECT_HTTP_AUTHORIZATION', '')
        if auth:
            environ['HTTP_AUTHORIZATION'] = auth
    return _application(environ, start_response)
```

### File `.htaccess` (di folder `api/`)
```apache
RewriteEngine On
RewriteCond %{HTTP:Authorization} .
RewriteRule ^ - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
```

### File `.env` Produksi
```env
SECRET_KEY=your-very-long-random-secret-key
DEBUG=False
ALLOWED_HOSTS=checkin.dsti-ums.id

DB_USER=nama_db_user
DB_PASSWORD=password_db
DB_HOST=localhost
DB_PORT=3306
DB_NAME=nama_database

CORS_ALLOWED_ORIGINS=https://checkin.dsti-ums.id
```

### Deploy Pertama Kali
```bash
cd /home/umsbirot/checkin.dsti-ums.id/api

# Install dependencies
pip install -r requirements.txt

# Migrasi database
python manage.py migrate --settings=config.settings.production

# Seed data awal
python manage.py seed_data --settings=config.settings.production

# Collect static files
python manage.py collectstatic --noinput --settings=config.settings.production
cp -r staticfiles/. ../public_html/static/

# Restart app
touch passenger_wsgi.py
```

### Update Kode (Deployment Berikutnya)
```bash
cd /home/umsbirot/checkin.dsti-ums.id/api
git pull
pip install -r requirements.txt
python manage.py migrate --settings=config.settings.production
python manage.py collectstatic --noinput --settings=config.settings.production
cp -r staticfiles/. ../public_html/static/
touch passenger_wsgi.py
```

---

## 2.4 Konfigurasi Frontend Angular

### `public_html/.htaccess`
```apache
Options -MultiViews
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^ index.html [L]
```

> Wajib ada agar Angular routing tidak 404 saat halaman di-refresh.

---

## 2.5 Variabel Environment Lengkap

| Variabel | Keterangan | Contoh |
|----------|-----------|--------|
| `SECRET_KEY` | Django secret key (wajib) | random 50 karakter |
| `DEBUG` | Mode debug | `False` |
| `ALLOWED_HOSTS` | Domain yang diizinkan | `checkin.dsti-ums.id` |
| `DB_USER` | Username database MySQL | `dsti_user` |
| `DB_PASSWORD` | Password database MySQL | `••••••••` |
| `DB_HOST` | Host database | `localhost` |
| `DB_PORT` | Port database | `3306` |
| `DB_NAME` | Nama database | `dsti_attendance` |
| `CORS_ALLOWED_ORIGINS` | Origin frontend yang diizinkan | `https://checkin.dsti-ums.id` |
