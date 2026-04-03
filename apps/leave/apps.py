from django.apps import AppConfig


class LeaveConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.leave'
    verbose_name = 'Izin & Cuti'

    def ready(self):
        import apps.leave.signals  # noqa
