from django.apps import AppConfig
from user_auth.celery import debug_task

class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
    # Подключил сигналы
    def ready(self):
        import users.signals