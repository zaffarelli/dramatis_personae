'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
from collector.models.character import Character
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.contrib import admin
import logging

logger = logging.getLogger(__name__)

CYBERFEATURE_CATEGORIES = (
    ('0',"Trait"),
    ('1',"Attachment"),
    ('2',"Power Source"),
    ('3',"Look"),
    ('4',"Material"),
    ('5',"Quality"),
    ('6',"Technology"),
)

class Cyberfeature(models.Model):
    class Meta:
        verbose_name = "References: Cyberfeature"
    reference = models.CharField(max_length=64)
    value = models.IntegerField(default=1)
    complexity = models.IntegerField(default=1)
    tech_level = models.IntegerField(default=5)
    incompatibility = models.IntegerField(default=0)
    value = models.IntegerField(default=1)
    value_ratio = models.FloatField(default=0.0)
    category = models.CharField(max_length=20,choices=CYBERFEATURE_CATEGORIES,default='Trait',blank=True)
    description = models.TextField(default='',blank=True,max_length=1024)
    def __str__(self):
        return "%s (%s)"%(self.reference,CYBERFEATURE_CATEGORIES[int(self.category)][1])

class CyberwareRef(models.Model):
    class Meta:
        verbose_name = "References: Cyberware"
    reference = models.CharField(max_length=64)
    cyberfeatures = models.ManyToManyField(Cyberfeature, blank=True)
    complexity = models.IntegerField(default=0)
    value = models.IntegerField(default=0)
    surgery_cost = models.IntegerField(default=0)
    incompatibility = models.IntegerField(default=0)
    tech_level = models.IntegerField(default=0)
    description = models.TextField(default='',blank=True,max_length=1024)

    @property
    def features(self):
        lst = []
        for f in self.cyberfeatures.all():
            lst.append(f.reference)
        return ", ".join(lst)

    def __str__(self):
        return "%s"%(self.reference)

    def fix(self):
        try:
            self.value = 0
            self.incompatibility = 0
            self.complexity = 0
            global_ratio = 0.0
            self.tech_level = 0
            for f in self.cyberfeatures.all():
                if f.value>0:
                    self.value += f.value
                if f.value_ratio>0.0:
                    global_ratio += f.value_ratio
                self.incompatibility += f.incompatibility
                if f.tech_level > self.tech_level:
                    self.tech_level = f.tech_level
                self.complexity += f.complexity
            self.value += self.complexity * 10
            self.value *= 1.0+global_ratio
        except:
            logger.info("Device [%s] not yet fixable... Next save will do."%(self.reference))

@receiver(pre_save, sender=CyberwareRef, dispatch_uid='update_cyberware_ref')
def update_cyberware_ref(sender, instance, **kwargs):
    instance.fix()

class Cyberware(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    cyberware_ref = models.ForeignKey(CyberwareRef, on_delete=models.CASCADE)
    replacement_for = models.CharField(max_length=64,default='Add on')
    def __str__(self):
        return '%s (%s: %s)' % (self.character.full_name,self.replacement_for,self.cyberware_ref.reference)

# ADMIN

class CyberfeatureAdmin(admin.ModelAdmin):
    ordering = ('category','reference',)
    list_display = ['reference','category','complexity','tech_level','incompatibility','value','value_ratio','description']

class CyberwareRefAdmin(admin.ModelAdmin):
    ordering = ('reference',)
    list_display = ['reference','tech_level','value','incompatibility','features','description']

# class CyberwareAdmin(admin.ModelAdmin):
#     ordering = ('character','replacement_for','cyberware_ref')
#     list_display = ['character','replacement_for','cyberware_ref']
