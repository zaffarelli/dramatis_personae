'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.apps import AppConfig

class CollectorConfig(AppConfig):
    name = 'collector'

    def ready(self):
        import collector.signals.user
        import collector.signals.coc7
        import collector.signals.skill
        import collector.signals.benefice_affliction
        import collector.signals.character