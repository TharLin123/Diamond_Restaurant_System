from django.apps import AppConfig


class StaffConfig(AppConfig):
    name = 'staff'

    def ready(self):
        import staff.signals