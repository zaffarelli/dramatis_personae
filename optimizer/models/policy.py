"""
╔╦╗╔═╗  ╔═╗┌─┐┌┬┐┬┌┬┐┬┌─┐┌─┐┬─┐
 ║║╠═╝  ║ ║├─┘ │ │││││┌─┘├┤ ├┬┘
═╩╝╩    ╚═╝┴   ┴ ┴┴ ┴┴└─┘└─┘┴└─
"""
from django.db import models
from collector.models.character import Character
from datetime import datetime
from django.contrib import admin
import logging

logger = logging.getLogger(__name__)

class Policy(models.Model):
    class Meta:
        ordering = ['name']
        verbose_name = 'Optimizer: Character Policy'
    name = models.CharField(max_length=256, unique=True)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    is_armored = models.BooleanField(default=False, blank=True)
    is_armed = models.BooleanField(default=False, blank=True)
    is_balanced = models.BooleanField(default=False, blank=True)
    has_species_lifepath = models.BooleanField(default=False)
    has_standard_lifepath = models.BooleanField(default=False)
    has_tods_lifepath = models.BooleanField(default=False)
    is_applied = models.BooleanField(default=False, blank=True)
    pub_date = models.DateTimeField('Date published', default=datetime.now)
    last_comment = models.TextField(max_length=1024,default='',blank=True)

    def __str__(self):
        return "P:%s"%(self.name)

    def fix(self):
        self.name = f'{self.character.full_name} policy'

    def perform(self):
        self.character.save()
        self.is_applied = self.checkToDs()
        return self.last_comment

    def checkToDs(self):
        logger.debug('Check tods !!!! ')
        answer = True
        self.last_comment = ""
        tsk = []
        histories = {'10':0,'20':0, '30':0, '40':0, '50':0}
        if self.character.use_history_creation:
            # for tod in self.character.tourofduty_set.all():
            #     if not tod.tour_of_duty_ref.valid:
            #         tsk.append(f'--> *{tod.tour_of_duty_ref.reference}* is not a valid Tour of Duty.')
            #         answer = False
            if not self.character.nameless:
                for tod in self.character.tourofduty_set.all():
                    if tod.tour_of_duty_ref.category in ['10','20','30', '40', '50']:
                        histories[tod.tour_of_duty_ref.category] += tod.tour_of_duty_ref.value
                if (histories['10'] == 20) and (histories['20'] == 25) and (histories['30'] == 48) and (histories['50'] == 7):
                    tsk.append('Basic lifepath is ok.')
                else:
                    tsk.append(f'Broken lifepath --> {histories}')
                    answer = False
                #tsk.append(f' Number of ToDS: {histories["40"]/10}')
                #self.character.tod_count = histories["40"]/10
                self.has_standard_lifepath = answer
        if answer:
            if self.character.life_path_total == self.character.OP:
                tsk.append(f'Character balance is ok.')
            else:
                tsk.append(f'Unbalanced character !')
            self.is_balanced = answer
        self.last_comment = "\n".join(tsk)
        logger.info(self.last_comment)
        return answer

class PolicyAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ['name','character','last_comment','is_applied','has_standard_lifepath']