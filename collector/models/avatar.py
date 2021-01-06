"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from django.db import models
from datetime import datetime
from scenarist.models.epics import Epic
import logging

logger = logging.getLogger(__name__)


class Avatar(models.Model):
    class Meta:
        abstract = True
    full_name = models.CharField(max_length=200)
    rid = models.CharField(max_length=200, default='none')
    birthdate = models.IntegerField(default=0)
    gender = models.CharField(max_length=30, default='female')
    age = models.IntegerField(default=0)
    player = models.CharField(max_length=200, default='', blank=True)
    height = models.IntegerField(default=150)
    weight = models.IntegerField(default=50)
    narrative = models.TextField(default='', blank=True)
    entrance = models.CharField(max_length=100, default='', blank=True)
    keyword = models.CharField(max_length=32, blank=True, default='new')
    stars = models.CharField(max_length=256, blank=True, default='')
    importance = models.PositiveIntegerField(default=1)
    is_visible = models.BooleanField(default=True)
    is_dead = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    is_partial = models.BooleanField(default=True)
    spotlight = models.BooleanField(default=False)
    priority = models.BooleanField(default=False)
    need_pdf = models.BooleanField(default=False)
    need_fix = models.BooleanField(default=False)
    epic = models.ForeignKey(Epic, null=True, blank=True, on_delete=models.SET_NULL)
    pub_date = models.DateTimeField('Date published', default=datetime.now)

    def fix(self, conf=None):
        if conf is None:
            from collector.utils.basic import get_current_config
            conf = get_current_config()
        logger.warning(f'Fixing ........: {self.full_name}')
        if self.rid == 'none':
            self.get_rid(self.full_name)
        if self.player == 'none':
            self.player = ''
        if self.birthdate < 1000:
            self.birthdate = conf.epic.era - self.birthdate
            self.age = conf.epic.era - self.birthdate

    def get_rid(self, s):
        self.rid = Avatar.find_rid(s)

    @classmethod
    def find_rid(self, s):
        x = s.replace(' ', '_').replace("'", '').replace('é', 'e') \
            .replace('è', 'e').replace('ë', 'e').replace('â', 'a') \
            .replace('ô', 'o').replace('"', '').replace('ï', 'i') \
            .replace('à', 'a').replace('-', '')
        rid = x.lower()
        return rid

    def roll_attributes(self):
        pass