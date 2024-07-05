from django.apps import AppConfig


class RrhhConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "rrhh"

    def ready(self):
        # Importa la señal
        from . import signals
