"""
╔╦╗╔═╗  ╔═╗┌─┐┌─┐┌┐┌┌─┐┬─┐┬┌─┐┌┬┐
 ║║╠═╝  ╚═╗│  ├┤ │││├─┤├┬┘│└─┐ │
═╩╝╩    ╚═╝└─┘└─┘┘└┘┴ ┴┴└─┴└─┘ ┴
"""
from django.db import models
from django.contrib import admin
from django.urls import reverse
from scenarist.models.story_models import StoryModel
from scenarist.models.epics import Epic
import json


class Card(StoryModel):
    class Meta:
        ordering = ['chapter', 'name']

    epic = models.ForeignKey(Epic, null=True, on_delete=models.CASCADE)
    from scenarist.models.backlogs import Backlog
    backlogs = models.ManyToManyField(Backlog, blank=True)

    def __str__(self):
        str = f'{self.get_card_type_display().upper()}: {self.name}'
        return str

    @property
    def full_chapter(self):
        return f"CARD:{self.id}.{self.name}"

    def get_casting(self):
        """ Bring all avatars rids from all relevant text fields"""
        casting = super().get_casting()
        casting.append(self.fetch_avatars(self.resolution))
        return casting

    @property
    def get_tags(self):
        from scenarist.utils.tools import adventure_tag
        list = []
        list.append(adventure_tag("BATTLE", self.battle_scene,"#b51e1e"))
        list.append(adventure_tag("CHASE", self.chase_scene,"#8bce32"))
        list.append(adventure_tag("ACTION", self.action_scene,"#ce9232"))
        list.append(adventure_tag("TECHNICAL", self.technical_scene,"#29bdea"))
        list.append(adventure_tag("SPIRITUAL", self.spiritual_scene,"#6f3ad7"))
        list.append(adventure_tag("POLITICAL", self.political_scene,"#9b5583"))
        list.append(adventure_tag("DOWNTIME", self.downtime_scene,"#9e9e9e"))
        return " ".join(list)

    def get_absolute_url(self):
        return reverse('note-detail', kwargs={'pk': self.pk})

    @property
    def linked_backlogs(self):
        list = []
        for item in self.backlogs.all():
            list.append(item.name)
        return list

    @property
    def linked_backlogs_str(self):
        str = "<ul><li>" + "</li><li>".join(self.linked_backlogs) + "</li></ul>"
        return str

    @property
    def get_full_id(self):
        self.full_id = ""
        if self.card_type == "EP":
            self.full_id = f""
        return f':{int(self.chapter):02}'

    def set_pdf(self, value=True):
        self.to_PDF = value

    @property
    def action_model(self):
        str = self.__class__.__name__
        return str.lower()

    def to_json(self):
        """ Returns JSON of object """
        from scenarist.utils.tools import json_default
        jst = super().to_json()
        job = json.loads(jst)
        # job['fullchapter'] = self.full_chapter
        job['tags'] = self.get_tags
        job['action_model'] = self.action_model
        return job


CARDS_RELATIONSHIPS = (
    ('UN', 'Undefined'),
    ('PO', 'Parent of'),
    ('EX', 'Explains'),
    ('CO', 'consequence of'),
)


class CardLink(models.Model):
    cardin = models.ForeignKey(Card, on_delete=models.CASCADE, null=True, related_name='cardin')
    cardout = models.ForeignKey(Card, on_delete=models.CASCADE, null=True, related_name='cardout')
    label = models.CharField(default='UN', max_length=30, choices=CARDS_RELATIONSHIPS)
    param = models.IntegerField(default=1)


class CardLinkInline(admin.TabularInline):
    fk_name = 'cardin'
    model = CardLink
    extras = 3
    ordering = ('cardin', 'cardout')


class CardLinkAdmin(admin.ModelAdmin):
    ordering = ['label']
    list_display = ['cardin', 'cardout', 'label', 'param']


class CardAdmin(admin.ModelAdmin):
    ordering = ['chapter', 'name']
    list_display = ['name', 'epic', 'card_type', 'temporary', 'full_id', 'chapter', 'date', 'dt', 'place',
                    'description']
    list_filter = ['epic', 'card_type', 'temporary', 'place', 'date']
    search_fields = ['description', 'name', 'resolution']
    list_editable = ['epic', 'temporary', 'card_type', 'full_id']
    inlines = [CardLinkInline]
