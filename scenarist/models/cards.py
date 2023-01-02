"""
╔╦╗╔═╗  ╔═╗┌─┐┌─┐┌┐┌┌─┐┬─┐┬┌─┐┌┬┐
 ║║╠═╝  ╚═╗│  ├┤ │││├─┤├┬┘│└─┐ │
═╩╝╩    ╚═╝└─┘└─┘┘└┘┴ ┴┴└─┴└─┘ ┴
"""
from django.db import models
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from scenarist.models.story_models import StoryModel
from scenarist.models.epics import Epic
import json


class Card(StoryModel):
    class Meta:
        ordering = ['full_id', 'name']

    epic = models.ForeignKey(Epic, null=True, on_delete=models.CASCADE, blank=True)
    parent = models.ForeignKey('self', unique=False, related_name='ChildrenCards', on_delete=models.SET_NULL, null=True,
                               blank=True)
    abstract = models.CharField(default='', max_length=256, blank=True)

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
        list.append(adventure_tag("BATTLE", self.battle_scene, "#b51e1e"))
        list.append(adventure_tag("CHASE", self.chase_scene, "#326b41"))
        list.append(adventure_tag("ACTION", self.action_scene, "#b9471a"))
        list.append(adventure_tag("TECHNICAL", self.technical_scene, "#520b76"))
        list.append(adventure_tag("SPIRITUAL", self.spiritual_scene, "#6f3ad7"))
        list.append(adventure_tag("POLITICAL", self.political_scene, "#1a3cb9"))
        list.append(adventure_tag("DOWNTIME", self.downtime_scene, "#585858"))
        return " ".join(list)

    @property
    def card_type_color(self):
        prefix = {
            'EP': '#cc5f29',
            'DR': '#cc6d3d',
            'AC': '#cc7b52',
            'AD': '#85cc3d',
            'SC': '#8fcc52',
            'EV': '#3dcc6d',
            'SH': '#b8b8e6',
            'BK': '#3d3dcc',
            'UN': '#C0C0C0',
        }
        return prefix[self.card_type]

    @property
    def card_tag(self):
        from scenarist.utils.tools import card_tag
        list = []
        list.append(card_tag(self.card_type_prefix, self.card_type_color))
        return " ".join(list)

    def get_absolute_url(self):
        return reverse('card-detail', kwargs={'pk': self.id})

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

    def set_pdf(self, value=True):
        self.to_PDF = value

    @property
    def action_model(self):
        str = self.__class__.__name__
        return str.lower()

    @property
    def to_json(self):
        """ Returns JSON of object """
        jst = super().to_json()
        job = json.loads(jst)
        job['tags'] = self.get_tags
        job['card_tag'] = self.card_tag
        job['action_model'] = self.action_model
        return job

    @property
    def saved(self):
        return self._state.adding == False

    @property
    def card_type_prefix(self):
        prefix = {
            'EP': 'EPI',
            'DR': 'DRA',
            'AC': 'ACT',
            'SH': 'SCH',
            'BK': 'BKL',
            'AD': 'INT',
            'EV': 'EVE',
            'SC': 'SCE',
            'UN': '',
        }
        return prefix[self.card_type]

    @property
    def links(self):
        lst = []
        if self.saved:
            cardlinks = self.cardin.all()
            for link in cardlinks:
                lst.append(f'<li>{link.get_label_display()}: {link.cardout.name}</li>')
        return mark_safe("<ul>" + " ".join(lst) + '</ul>')

    def fix(self):
        if not self.epic:
            from collector.utils.basic import get_current_config
            self.epic = get_current_config().epic
        if self.parent:
            self.full_id = f"{self.parent.full_id}:{self.card_type_prefix}.{int(self.chapter):03}"
        else:
            if self.card_type == 'EP':
                self.full_id = f"{self.card_type_prefix}.{int(self.chapter):03}"
        adventure = None
        # if self.saved:
        #     cardlinks = self.cardin.all()
        #     for link in cardlinks:
        #         print(link)
        #         if link.label == 'CH':
        #             self.full_id = f'{link.cardout.full_id}:{self.card_type_prefix}{self.chapter:03}'
        #             adventure = link.cardout
        # if adventure:
        #     from datetime import timedelta
        #     if self.card_type in ["EV", "SC", "AD", "DR", "SH"]:
        #         self.dt = adventure.dt + timedelta(days=self.date_offset)
        if self.card_type in ['EP', 'DR', 'AC', 'SH', 'EV', 'BK']:
            self.battle_scene = False
            self.action_scene = False
            self.downtime_scene = False
            self.chase_scene = False


CARDS_RELATIONSHIPS = (
    ('UN', 'Undefined'),
    ('PO', 'Parent of'),
    ('EX', 'Explains'),
    ('CO', 'consequence of'),
    ('CH', 'Child of'),
)


class CardLink(models.Model):
    cardin = models.ForeignKey(Card, on_delete=models.CASCADE, null=True, related_name='cardin')
    cardout = models.ForeignKey(Card, on_delete=models.CASCADE, null=True, related_name='cardout')
    label = models.CharField(default='UN', max_length=30, choices=CARDS_RELATIONSHIPS)
    param = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.cardin} --({self.label})-> {self.cardout}"

    @property
    def short(self):
        return f"{self.get_label_display()} --> {self.cardout.full_id}"


class CardLinkInline(admin.TabularInline):
    fk_name = 'cardin'
    model = CardLink
    extras = 2
    ordering = ('cardin', 'cardout')


class CardLinkAdmin(admin.ModelAdmin):
    ordering = ['label']
    list_display = ['cardin', 'cardout', 'label', 'param']


def fix_all(modeladmin, request, queryset):
    for item in queryset:
        item.save()
    short_description = "Fix All"


class CardAdmin(admin.ModelAdmin):
    ordering = ['full_id']
    list_display = ['name', 'card_type', 'temporary', 'full_id', 'chapter', 'date_offset', 'dt', 'place',
                    'links']
    list_filter = ['epic', 'card_type', 'temporary', 'place']
    search_fields = ['description', 'name', 'resolution']
    list_editable = ['temporary', 'card_type', 'date_offset', 'chapter']
    inlines = [CardLinkInline]
    actions = [fix_all]
