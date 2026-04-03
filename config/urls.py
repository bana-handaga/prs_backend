from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/v1/', include([
        path('auth/', include('apps.accounts.urls_auth')),
        path('staff/', include('apps.accounts.urls_staff')),
        path('departments/', include('apps.accounts.urls_dept')),
        path('schedules/', include('apps.attendance.urls_schedule')),
        path('attendance/', include('apps.attendance.urls')),
        path('leave/', include('apps.leave.urls')),
        path('reports/', include('apps.reports.urls')),
        path('holidays/', include('apps.attendance.urls_holiday')),
    ])),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
