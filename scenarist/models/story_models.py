"""
╔╦╗╔═╗  ╔═╗┌─┐┌─┐┌┐┌┌─┐┬─┐┬┌─┐┌┬┐
 ║║╠═╝  ╚═╗│  ├┤ │││├─┤├┬┘│└─┐ │
═╩╝╩    ╚═╝└─┘└─┘┘└┘┴ ┴┴└─┴└─┘ ┴
"""
from django.db import models
import re
import string
import json
from django.utils import timezone

CARD_TYPES = (
    ('UN', 'Uncategorized'),
    ('SC', 'Scene'),
    ('EV', 'Event'),
    ('BK', 'Background'),
    ('AC', 'Act'),
    ('EP', 'Epic'),
    ('SH', 'Scheme'),
    ('AD', 'Adventure'),
    ('NO', 'Note'),
    ('DR', 'Drama'),
)


class StoryModel(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(default='', max_length=256, blank=True, unique=True)
    #chapter = models.CharField(default='0', max_length=12, blank=True)
    chapter = models.PositiveIntegerField(default=0, blank=True)
    date_offset = models.IntegerField(default=0, blank=True)
    dt = models.DateTimeField(default=timezone.now, blank=True, null=True)
    sdt = models.DateTimeField(default=timezone.now, blank=True, null=True)
    place = models.CharField(max_length=128, default='', blank=True)
    gamemaster = models.CharField(default='zaffarelli@gmail.com', max_length=128, blank=True)
    visible = models.BooleanField(default=True)
    battle_scene = models.BooleanField(default=False)
    chase_scene = models.BooleanField(default=False)
    action_scene = models.BooleanField(default=False)
    technical_scene = models.BooleanField(default=False)
    spiritual_scene = models.BooleanField(default=False)
    political_scene = models.BooleanField(default=False)
    roleplay_scene = models.BooleanField(default=False)
    business_scene = models.BooleanField(default=False)
    mystery_scene = models.BooleanField(default=False)
    downtime_scene = models.BooleanField(default=False)
    to_PDF = models.BooleanField(default=True)
    temporary = models.BooleanField(default=True)
    full_id = models.CharField(max_length=64, blank=True, default='')
    description = models.TextField(max_length=6000, default='', blank=True)
    resolution = models.TextField(default='', max_length=2560, blank=True)
    rewards = models.TextField(max_length=1024, default='', blank=True)
    card_type = models.CharField(max_length=2, default='UN', choices=CARD_TYPES, blank=True)
    archived = models.BooleanField(default=False)
    is_ongoing = models.BooleanField(default=False)


    def __str__(self):
        """ Standard display """
        return f"{self.chapter} {self.name}"

    @property
    def minis(self):
        from collector.models.character import Character
        casting = self.get_full_cast()
        list = []
        for c in casting:
            ch = Character.objects.filter(rid=c).first()
            if ch.player == "":
                if not ch in list:
                    list.append(ch)
        return list

    def to_json(self):
        """ Returns JSON of object """
        from scenarist.utils.tools import json_default
        return json.dumps(self, default=json_default, sort_keys=True, indent=4)

    @property
    def children(self):
        arr = []
        for episode in self.get_episodes():
            arr.append("%s_%d" % (type(episode).__name__.lower(), episode.id))
        return ";".join(arr)

    def fetch_avatars(self, value):
        """ Bring all avatars rids from some text"""
        from collector.models.character import Character
        avar = []
        seeker = re.compile('\¤(\w+)\¤')
        changes = []
        res = str(value)
        iter = seeker.finditer(res)
        for item in iter:
            rid = ''.join(item.group().split('¤'))
            ch = Character.objects.filter(rid=rid).first()
            if ch is not None:
                ch.is_cast = True
                ch.save()
                avar.append(ch.rid)
        return avar

    def got(self, rid):
        list = self.fetch_avatars(self.description)
        try:
            list += self.fetch_avatars(self.resolution)
        except:
            pass
        try:
            _ = list.index(rid)
        except ValueError:
            return False
        else:
            return True

    def get_casting(self):
        """ Bring all avatars rids from all relevant text fields"""
        casting = []
        casting.append(self.fetch_avatars(self.description))
        return casting

    def get_episodes(self):
        """ Return subchapters """
        return []

    def get_full_cast(self):
        """ Return the depth cast for this episode """
        casting = self.get_casting()
        for episode in self.get_episodes():
            casting.append(episode.get_full_cast())
        flat_cast = [c for subcast in casting for c in subcast]
        new_list = sorted(list(set(flat_cast)))
        print(new_list)
        return new_list

    @property
    def get_full_id(self):
        """ Return subchapters """
        return f'{self.id}'

    def turn_into_note(self):
        if self.card_type == 'UN':
            self.card_type = 'NO'
            self.save()



