from .base import *
import dj_database_url

DEBUG = False

DATABASES = {
    'default': dj_database_url.config(
        default=(
            f"mysql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}"
            f"@{os.environ.get('DB_HOST', '127.0.0.1')}:{os.environ.get('DB_PORT', '3306')}"
            f"/{os.environ.get('DB_NAME', 'dsti_attendance')}"
        )
    )
}

SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
