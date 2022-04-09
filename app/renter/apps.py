from django.apps import AppConfig


class RenterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'renter'

    def ready(self):
        from renter import signals

