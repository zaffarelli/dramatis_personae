from django.db import models
from collector.models.characters import Character
from django.contrib import admin

class WeaponRef(models.Model):
  reference = models.CharField(max_length=64,default='',blank=True, unique=True)
  category = models.CharField(max_length=5,choices=(('MELEE',"Melee weapon"),('P',"Pistol/revolver"),('RIF',"Rifle"),('SMG',"Submachinegun"),('SHG',"Shotgun"),('HVY',"Heavy weapon"),('EX',"Exotic weapon")),default='RIF',blank=True)
  weapon_accuracy = models.IntegerField(default=0,blank=True)
  conceilable = models.CharField(max_length=1,choices=(('P',"Pocket"),('J',"Jacket"),('L',"Long coat"),('N',"Can't be hidden")),default='J',blank=True)
  availability = models.CharField(max_length=1,choices=(('E',"Excellent"),('C',"Common"),('P',"Poor"),('R',"Rare")),default='C',blank=True)
  damage_class = models.CharField(max_length=16,default='',blank=True)
  caliber = models.CharField(max_length=16,default='',blank=True)
  str_min = models.PositiveIntegerField(default=0,blank=True)
  rof = models.PositiveIntegerField(default=0,blank=True)
  clip = models.PositiveIntegerField(default=0,blank=True)
  rng = models.PositiveIntegerField(default=0,blank=True)
  rel = models.CharField(max_length=2,choices=(('VR',"Very reliable"),('ST',"Standard"),('UR',"Unreliable")),default='ST',blank=True)
  cost = models.PositiveIntegerField(default=0,blank=True)
  description = models.TextField(max_length=256,default='',blank=True)
  def __str__(self):
    return '%s (%s/%s/%s/%s£)' % (self.reference, self.category, self.damage_class, self.caliber, self.cost)

class Weapon(models.Model):
  character = models.ForeignKey(Character, on_delete=models.CASCADE)
  weapon_ref = models.ForeignKey(WeaponRef, on_delete=models.CASCADE)
  ammoes = models.PositiveIntegerField(default=0,blank=True)
  def __str__(self):
    return '%s=%s' % (self.character.full_name,self.weapon_ref.reference)

class WeaponRefAdmin(admin.ModelAdmin):
  ordering = ('category','reference',)  

class WeaponAdmin(admin.ModelAdmin):
  ordering = ('character','weapon_ref',)



