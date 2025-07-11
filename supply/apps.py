from django.apps import AppConfig


class SupplyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'supply'

    def ready(self):
        import supply.signals  # Import signals when app is ready