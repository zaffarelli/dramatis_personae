'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
from django.contrib import admin

class WeaponRef(models.Model):
  class Meta:
    ordering = ['origins','reference', 'category','damage_class',]
    verbose_name = "Weapon Reference"    
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
  stats = models.CharField(max_length=256,default='',blank=True)
  origins = models.CharField(max_length=64,default='',blank=True)
  def __str__(self):
    return '%s' % (self.stats)
  def get_stats_line(self):
    res = []
    res.append(self.reference)
    res.append(self.category)
    res.append('WA:'+str(self.weapon_accuracy))
    res.append(self.conceilable)
    res.append(self.availability)
    res.append('DC:'+self.damage_class)
    if self.category == 'MELEE':
      res.append('STR:'+str(self.str_min))
    else:
      res.append('Cal:'+self.caliber)
      res.append('ROF:'+str(self.rof))
      res.append('Clip:'+str(self.clip))
    res.append('RNG:'+str(self.rng))    
    res.append(str(self.rel))
    res.append('£'+str(self.cost))
    self.stats = ' . '.join(res) # ⦁⏺
    self.save()
    return self.stats


class Weapon(models.Model):
  from collector.models.character import Character
  character = models.ForeignKey(Character, on_delete=models.CASCADE)
  weapon_ref = models.ForeignKey(WeaponRef, on_delete=models.CASCADE)
  ammoes = models.PositiveIntegerField(default=0,blank=True)
  def __str__(self):
    return '%s=%s' % (self.character.full_name,self.weapon_ref.reference)

def update_stats_lines(modeladmin, request, queryset):
  selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
  for w in selected:
    WeaponRef.objects.get(pk=w).get_stats_line()
  short_description = "Update stats line"

class WeaponRefAdmin(admin.ModelAdmin):
  list_display = ('reference','origins','category','weapon_accuracy','damage_class','availability','cost')
  ordering = ('origins','reference','category','damage_class',)
  actions = [update_stats_lines,]




