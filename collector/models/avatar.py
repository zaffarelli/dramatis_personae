"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from django.db import models
from datetime import datetime
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

    pub_date = models.DateTimeField('Date published', default=datetime.now)

    def fix(self, conf=None):
        logger.warning(f'Fixing ........: {self.full_name}')
        if self.rid == 'none':
            self.get_rid(self.full_name)
        if self.player == 'none':
            self.player = ''

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