from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.accounts.permissions import IsAdmin, IsAdminOrSupervisor
from .models import LeaveType, LeaveRequest
from .serializers import (
    LeaveTypeSerializer, LeaveRequestSerializer,
    LeaveRequestCreateSerializer, ReviewSerializer, LeaveBalanceSerializer
)


class LeaveTypeViewSet(viewsets.ModelViewSet):
    queryset = LeaveType.objects.filter(is_active=True)
    serializer_class = LeaveTypeSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]


class LeaveRequestViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'leave_type']
    search_fields = ['staff__full_name', 'staff__employee_id']
    ordering_fields = ['created_at', 'start_date']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = LeaveRequest.objects.select_related('staff', 'leave_type', 'reviewed_by')
        if self.request.user.role in ('admin', 'supervisor'):
            return qs
        return qs.filter(staff=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return LeaveRequestCreateSerializer
        return LeaveRequestSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Staff can only cancel their own PENDING requests
        if request.user.role == 'staff':
            if instance.staff != request.user:
                return Response({'detail': 'Tidak diizinkan.'}, status=status.HTTP_403_FORBIDDEN)
            if instance.status != 'menunggu':
                return Response(
                    {'detail': 'Hanya permohonan dengan status "Menunggu" yang dapat dibatalkan.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            instance.status = 'dibatalkan'
            instance.save()
            return Response(LeaveRequestSerializer(instance).data)
        return Response({'detail': 'Tidak diizinkan.'}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminOrSupervisor])
    def approve(self, request, pk=None):
        instance = self.get_object()
        if instance.status != 'menunggu':
            return Response(
                {'detail': 'Hanya permohonan dengan status "Menunggu" yang dapat disetujui.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance.status = 'disetujui'
        instance.reviewed_by = request.user
        instance.reviewed_at = timezone.now()
        instance.review_note = serializer.validated_data.get('review_note', '')
        instance.save()
        return Response(LeaveRequestSerializer(instance).data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminOrSupervisor])
    def reject(self, request, pk=None):
        instance = self.get_object()
        if instance.status != 'menunggu':
            return Response(
                {'detail': 'Hanya permohonan dengan status "Menunggu" yang dapat ditolak.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance.status = 'ditolak'
        instance.reviewed_by = request.user
        instance.reviewed_at = timezone.now()
        instance.review_note = serializer.validated_data.get('review_note', '')
        instance.save()
        return Response(LeaveRequestSerializer(instance).data)


class LeaveBalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        year = timezone.now().year
        leave_types = LeaveType.objects.filter(is_active=True)
        result = []
        for lt in leave_types:
            from django.db.models import Sum
            used_days = LeaveRequest.objects.filter(
                staff=request.user,
                leave_type=lt,
                status='disetujui',
                start_date__year=year
            ).aggregate(total=Sum('total_days'))['total'] or 0

            remaining = None
            if lt.max_days_per_year is not None:
                remaining = max(0, lt.max_days_per_year - used_days)

            result.append({
                'leave_type_id': lt.id,
                'leave_type_name': lt.name,
                'max_days': lt.max_days_per_year,
                'used_days': used_days,
                'remaining_days': remaining,
            })
        return Response(result)
