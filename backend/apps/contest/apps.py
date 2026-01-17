from django.apps import AppConfig

class ContestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.contest'
    verbose_name = '웅변대회'

    def ready(self):
        import apps.contest.signals
