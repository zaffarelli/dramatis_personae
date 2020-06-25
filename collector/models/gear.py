'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
from django.contrib import admin
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

import logging
logger = logging.getLogger(__name__)

REFERENCES = (
    ("FS2CRB","Fading Suns 2ed Core Rulebook"),
    ("DEM","Introduced in epic Deus Ex Machina"),
    ("ANTU","Introduced in epic Abusus Non Tollit Usum"),
    ("MotJ","Merchants of the Jumpweb"),
    ("FL:T","Forbidden Lore: Technology"),
    ("AT","Arcane Tech"),
    ("FSC","Fading Suns Companion"),
)

QUALITIES = (
    ("0","Poor"),
    ("1","Standard"),
    ("2","High"),
    ("3","Premium"),
    ("4","Deluxe"),
)

AVAILABILITIES = (
    ("0","Exotic"),
    ("1","Rare"),
    ("2","Uncommon"),
    ("3","Common"),
    ("4","Very Common"),
)

UNITS = (
    ("1","piece"),
    ("x10","x10 pieces"),
    ("x100","x100 pieces"),
    ("x1000","x1000 pieces"),
    ("litre","litre"),
    ("m3","cubic meter"),
    ("kg","kg"),
    ("g","g"),
    ("mg","mg"),
    ("day","day"),
    ("night","night"),
    ("week","week"),
    ("month","month"),
    ("year","year"),
    ("2","pair"),
)

CATEGORIES = (
    ("0","Miscellaneous"),
    ("1","Beverage/Food"),
    ("2","Medical Supplies"),
    ("3","Communications"),
    ("4","Tools"),
    ("5","Think Machines"),
    ("6","Drugs"),
    ("7","Clothing"),
    ("8","Vehicle"),
    ("9","Explosives"),
    ("10","Entertainment"),

)

MAGNA_CARTA_ENTRIES = (
    ("0","Legit"),
    ("1","Restricted Sell"),
    ("2","Restricted Usage"),
    ("3","Unauthorized"),
    ("4","Proscribed by the Church"),
)



class Gear(models.Model):
    class Meta:
        verbose_name = "References: Gear"
    name = models.CharField(max_length=128)
    variant = models.CharField(max_length=128,blank=True,null=True)
    category = models.CharField(choices=CATEGORIES,max_length=32,default='Miscellaneous',blank=True,null=True)
    magna_carta_entry = models.CharField(choices=MAGNA_CARTA_ENTRIES,default='0',max_length=32,blank=True,null=True)
    quality = models.CharField(choices=QUALITIES,default='Standard',max_length=32)
    availability = models.CharField(choices=AVAILABILITIES,default='Common',max_length=32,blank=True,null=True)
    quantity = models.PositiveIntegerField(default=1)
    unit = models.CharField(choices=UNITS,default='apiece',max_length=32,blank=True,null=True)
    origin = models.CharField(default='',max_length=128,blank=True,null=True)
    tech_level = models.PositiveIntegerField(default=4)
    price = models.FloatField(default=0.0)
    firebird_price = models.PositiveIntegerField(default=0)
    wing_price = models.PositiveIntegerField(default=0)
    crest_price = models.PositiveIntegerField(default=0)
    talon_price = models.PositiveIntegerField(default=0)
    description = models.TextField(default='',blank=True, max_length=2048)
    reference = models.CharField(choices=REFERENCES,default='FS2CRB',max_length=32,blank=True,null=True)

    def fix(self):
        self.price = self.firebird_price + self.crest_price / 2 + self.wing_price / 4 + self.talon_price / 8

@receiver(pre_save, sender=Gear, dispatch_uid='update_gear')
def update_gear(sender, instance, conf=None, **kwargs):
    instance.fix()

class GearAdmin(admin.ModelAdmin):
    ordering = ('category','name','variant','price')
    list_display = ['name','variant','category','quality','availability','tech_level','price','magna_carta_entry','reference']
    search_fields = ('name','variant','description')
    list_filter = ('tech_level','category','magna_carta_entry','origin','quality','reference')
