from collector.models.campaign import Campaign
from PIL import Image
#  exec(open('scripts/update_alliances.py').read())
from collector.models.character import Character
from collector.models.alliance_ref import AllianceRef

all = Character.objects.all()
for character in all:
    matching_alliance = AllianceRef.objects.filter(reference=character.alliance)
    if len(matching_alliance)>0:
        character.alliance_ref = matching_alliance.first()
        character.save()
        print(f'{character.full_name} --> Found {matching_alliance.first().reference} ')
