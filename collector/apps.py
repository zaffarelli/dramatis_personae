"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from django.apps import AppConfig


class CollectorConfig(AppConfig):
    name = 'collector'

    def ready(self):
        import collector.signals.user
        import collector.signals.skill
        import collector.signals.benefice_affliction
        import collector.signals.character
        import collector.signals.cyber
        import collector.signals.tod
        import collector.signals.armor
        import collector.signals.spacecraft
        import collector.signals.collection
