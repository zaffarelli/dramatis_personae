from django.apps import AppConfig


class CartographConfig(AppConfig):
    name = 'cartograph'

    def ready(self):
        import cartograph.signals.system
