from django.urls import path
from .views import (
    AttendanceReportView, AttendanceReportExportView,
    LeaveSummaryReportView, DepartmentSummaryReportView
)

urlpatterns = [
    path('attendance/', AttendanceReportView.as_view(), name='report-attendance'),
    path('attendance/export/', AttendanceReportExportView.as_view(), name='report-attendance-export'),
    path('leave/', LeaveSummaryReportView.as_view(), name='report-leave'),
    path('summary/', DepartmentSummaryReportView.as_view(), name='report-summary'),
]
