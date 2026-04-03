from rest_framework.routers import DefaultRouter
from .views import WorkScheduleViewSet

router = DefaultRouter()
router.register('', WorkScheduleViewSet, basename='schedule')

urlpatterns = router.urls
