from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import AttendanceViewSet, CheckInView, CheckOutView, TodayAttendanceView, AttendanceSummaryView

router = DefaultRouter()
router.register('', AttendanceViewSet, basename='attendance')

urlpatterns = [
    path('check-in/', CheckInView.as_view(), name='attendance-checkin'),
    path('check-out/', CheckOutView.as_view(), name='attendance-checkout'),
    path('today/', TodayAttendanceView.as_view(), name='attendance-today'),
    path('summary/', AttendanceSummaryView.as_view(), name='attendance-summary'),
] + router.urls
