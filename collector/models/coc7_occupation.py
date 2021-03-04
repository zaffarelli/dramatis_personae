"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from django.db import models
from django.contrib import admin
# from cartograph.models.investigator import Investigator


OCCUPATION_POINTS_METHODS = (
    ('METHOD_1','EDU x 4'),
    ('METHOD_2','EDU x 2 + DEX x 2'),
    ('METHOD_3','EDU x 2 + APP x 2'),
    ('METHOD_4','EDU x 2 + FOR x 2'),
    ('METHOD_5','EDU x 2 + (DEX x 2 ou FOR x 2)'),
    ('METHOD_6','EDU x 2 + (DEX x 2 ou POU x 2)'),
    ('METHOD_7','EDU x 2 + (APP x 2 ou DEX x 2)'),
    ('METHOD_8','EDU x 2 + (APP x 2 ou POU x 2)'),
    ('METHOD_9','EDU x 2 + (APP x 2 ou DEX x 2 ou FOR x 2)'),
)

class Coc7Occupation(models.Model):
    class Meta:
        ordering = ['reference']
        verbose_name = "COC7: Occupation"

    reference = models.CharField(max_length=200, unique=True)
    smart_code = models.CharField(max_length=200, default='TBD')
    is_classic = models.BooleanField(default=False)
    is_lovecraftian = models.BooleanField(default=False)
    occupation_points = models.CharField(max_length=128, choices=OCCUPATION_POINTS_METHODS,default='METHOD_1')
    credit_range = models.CharField(max_length=128,default='0;99')
    credit_min = models.PositiveIntegerField(default='0')
    credit_max = models.PositiveIntegerField(default='99')

    def __str__(self):
        c = l = ''
        if self.is_classic:
            c = '[C]'
        if self.is_lovecraftian:
            l = '[L]'
        return f'{self.reference}{c}{l}'

    def fix(self):
        from collector.utils.rpg import smart_code
        self.smart_code = smart_code(self.reference)
        creds = self.credit_range.split(';')
        self.credit_min = int(creds[0])
        self.credit_max = int(creds[1])

    @property
    def competences(self):
        list = []
        for x in self.coc7skillmodificator_set.all():
            list.append(x.skill_ref.reference)
        return ", ".join(list)

