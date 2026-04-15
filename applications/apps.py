from django.apps import AppConfig


class ApplicationConfig(AppConfig):
    name = 'applications'

class ApplicationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications'

    def ready(self):
        import applications.signals
