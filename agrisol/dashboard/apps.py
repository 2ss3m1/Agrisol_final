from django.apps import AppConfig


class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'

    def ready(self):
        from . import mqtt_client
        mqtt_client.start()
# class CulturesConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'cultures'

#     def ready(self):
#         from .. import signals