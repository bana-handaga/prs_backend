from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import LeaveTypeViewSet, LeaveRequestViewSet, LeaveBalanceView

router = DefaultRouter()
router.register('types', LeaveTypeViewSet, basename='leave-type')
router.register('requests', LeaveRequestViewSet, basename='leave-request')

urlpatterns = [
    path('balance/', LeaveBalanceView.as_view(), name='leave-balance'),
] + router.urls
