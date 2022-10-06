from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    # Добавление человеко понятного названия приложения в админке
    verbose_name = 'Главная страница'
