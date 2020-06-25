'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
from collector.models.character import Character
from django.contrib import admin
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

class Loot(models.Model):
    class Meta:
        verbose_name = "References: Loot"    
    name = models.CharField(max_length=128)
    group = models.CharField(max_length=128,default='',blank=True,null=True)
    price = models.PositiveIntegerField(default=0)
    session = models.PositiveIntegerField(default=0)
    description = models.TextField(default='',blank=True, max_length=2048)
    secret = models.TextField(default='',blank=True, max_length=2048)
    sleeves_authenticity = models.PositiveIntegerField(default=0)
    sleeves_gossip = models.PositiveIntegerField(default=0)
    sleeves_fame = models.PositiveIntegerField(default=0)
    sleeves_auction = models.PositiveIntegerField(default=100)
    sleeves_minimum_increment = models.PositiveIntegerField(default=100)
    index = models.PositiveIntegerField(default=0)
    owner = models.ForeignKey(Character, on_delete=models.SET_NULL, null=True, blank=True)
    code = models.CharField(max_length=128,default='',blank=True,null=True)

    def set_code(self):
        str = "".join(self.name.lower().split(":")[0])
        str = "_".join(str.split(" "))
        str = "_".join(str.split("-"))
        str = "".join(str.split("'"))
        str = "e".join(str.split("é"))
        self.code = str

@receiver(pre_save, sender=Loot, dispatch_uid='update_loot')
def update_loot(sender, instance, conf=None, **kwargs):
    instance.set_code()

class LootAdmin(admin.ModelAdmin):
    ordering = ('session','index','name','price')
    list_display = ['name','code','session','index','group','price','sleeves_authenticity','sleeves_gossip','sleeves_fame','sleeves_auction','sleeves_minimum_increment','owner','description']
