from django.apps import AppConfig


class TktGopaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tkt_GOPA'

    def ready(self):
        import tkt_GOPA.signals  # Importa las señales aquí