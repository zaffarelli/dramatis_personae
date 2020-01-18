from collector.models.characters import Character
from collector.models.tourofduty import TourOfDuty

all = Character.objects.filter(epic__shortcut="DEM")
for c in all:
    if c.player:
        c.use_history_creation = false
    if "urthish" in c.specie.species.lower():
        pass
    c.save()
