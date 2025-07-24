from django.apps import AppConfig


class Post_ListsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.post_lists'

    def ready(self):
        import apps.post_lists.signals
