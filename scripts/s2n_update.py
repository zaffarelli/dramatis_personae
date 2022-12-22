import sys
from collector.models.campaign import Campaign
from scenarist.models.epics import Epic
from scenarist.models.dramas import Drama
from scenarist.models.acts import Act
from scenarist.models.events import Event
from scenarist.models.cards import Card

# Run me through python manage.py shell, then:
# exec(open('scripts/s2n_update.py').read())
class S2NUpdater:
    def __init__(self):
        print("  This is dP updater script. Here is a list of actions...")
        print("    1 - Transform *standard* campaign to *notes* campaign.")
        print("    0 - Quit")
        topic = ''
        while topic != '0':
            topic = input('  What do you want to do? [0] ')
            if topic == '1':
                self.perform()

    def push2card(self, src, tgt):
        if isinstance(src,Epic):
            tgt.epic = src
        else:
            if isinstance(src, Drama):
                tgt.epic = src.epic
            else:
                if isinstance(src, Act):
                    tgt.epic = src.drama.epic
                else:
                    if isinstance(src, Event):
                        tgt.epic = src.act.drama.epic
        tgt.description = src.description
        tgt.place = src.place
        tgt.name = src.name
        tgt.data = src.date
        tgt.chapter = src.chapter
        tgt.temporary = True
        tgt.resolution = src.resolution
        tgt.rewards = src.rewards
        tgt.challenge = src.challenge
        tgt.full_id = src.full_id
        tgt.archived = src.archived
        tgt.visible = src.visible
        tgt.battle_scene = src.battle_scene
        tgt.chase_scene = src.chase_scene
        tgt.action_scene = src.action_scene
        tgt.technical_scene = src.technical_scene
        tgt.spiritual_scene = src.spiritual_scene
        tgt.political_scene = src.political_scene
        tgt.downtime_scene = src.downtime_scene

    def bf(self, txt):
        new_txt = "\033[1;39m".join(txt.split('µ'))
        new_txt = "\033[0;m".join(new_txt.split('§'))
        return new_txt

    def perform(self):
        print("  Select source campaign...")
        all = Campaign.objects.all()
        for c, i in enumerate(all):
            print(self.bf(f"    µ{c}§ - µ{i.epic.shortcut}§ [{i.epic.name}]"))
        print("    0 - None")
        action = ''
        while action != 'x':
            action = input('  Choice of campaign ? [x] ')
            if action != 'x':
                temp_cards = Card.objects.all()
                cnt_deleted = 0
                for card in temp_cards:
                    if card.temporary:
                        card.delete()
                        cnt_deleted += 1
                print(f" Deleted cards: {cnt_deleted}")
                src_epic = all[int(action)].epic
                print(f"{src_epic.name} {src_epic.era}")
                new_card = Card()
                new_card.card_type = 'EP'
                self.push2card(src_epic,new_card)
                new_card.save()
                for d in src_epic.drama_set.all():
                    print(f"      - Drama: {d.name} Chapter:{d.full_chapter}")
                    new_card = Card()
                    new_card.card_type = 'DR'
                    self.push2card(d, new_card)
                    new_card.save()
                    for a in d.act_set.all():
                        print(f"         - Act: {a.name} Chapter:{a.full_chapter}")
                        new_card = Card()
                        new_card.card_type = 'AC'
                        self.push2card(a, new_card)
                        new_card.save()
                        for e in a.event_set.all():
                            print(f"           - Event: {e.name} Chapter:{e.full_chapter}")
                            new_card = Card()
                            new_card.card_type = 'EV'
                            self.push2card(e, new_card)
                            new_card.save()


f = S2NUpdater()
