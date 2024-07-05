from django.apps import AppConfig
from django.db.models.signals import post_save

class ChartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'
    def ready(self):
        from . import signals

        ## explicitely connecting the signal handler with signals
        # post_save.connect(signals.post_save_handler,weak=False)

