"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from django.db import models
from django.contrib import admin
import json


CALIBERS = (
    ('n/a', 'n/a'),
    ('0.172', '0.172/4mm'),
    ('0.20', '0.20/5mm'),
    ('0.23', '0.23/6mm'),
    ('0.284', '0.284/7mm'),
    ('0.32', '0.32/8mm'),
    ('0.35', '0.35/9mm'),
    ('0.40', '0.40/10mm'),
    ('0.44', '0.44/11mm'),
    ('0.47', '0.47/12mm'),
    ('0.51', '0.51/13mm'),
    ('0.21', '0.21/5.56mm'),
    ('0.30', '0.30/7.62mm'),
    ('0.78', '0.78/20mm'),
)


class WeaponRef(models.Model):
    class Meta:
        ordering = ['meta_type', 'category', 'reference', 'origins', 'damage_class', ]
        verbose_name = "FICS: Weapon"

    reference = models.CharField(max_length=64, default='')
    meta_type = models.CharField(max_length=64, default='')
    category = models.CharField(max_length=5, choices=(
        ('MELEE', "Melee weapon"), ('P', "Pistol/revolver"), ('RIF', "Rifle"), ('SMG', "Submachinegun"),
        ('SHG', "Shotgun"),
        ('HVY', "Heavy weapon"), ('EX', "Exotic weapon"), ('SP', 'Special')), default='RIF')
    weapon_accuracy = models.IntegerField(default=0)
    conceilable = models.CharField(max_length=1, choices=(
        ('P', "Pocket"), ('J', "Jacket"), ('L', "Long coat"), ('N', "Can't be hidden")), default='J')
    availability = models.CharField(max_length=1,
                                    choices=(('E', "Excellent"), ('C', "Common"), ('P', "Poor"), ('R', "Rare")),
                                    default='C')
    damage_class = models.CharField(max_length=16, default='1D6')
    caliber = models.CharField(max_length=16, default='n/a', blank=True)
    fusion_cell = models.CharField(max_length=64, default='', blank=True)
    str_min = models.PositiveIntegerField(default=0)
    rof = models.PositiveIntegerField(default=0)
    clip = models.PositiveIntegerField(default=0)
    tech_level = models.PositiveIntegerField(default=5)
    rng = models.PositiveIntegerField(default=0)
    rel = models.CharField(max_length=2, choices=(('VR', "Very reliable"), ('ST', "Standard"), ('UR', "Unreliable")),
                           default='ST')
    cost = models.PositiveIntegerField(default=0)
    description = models.TextField(max_length=1024, default='', blank=True)
    stats = models.CharField(max_length=256, default='', blank=True)
    origins = models.CharField(max_length=64, default='', blank=True)
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return f'[{self.category}]{self.meta_type} {self.reference} '

    @property
    def get_damage_stats(self):
        min = 0
        max = 0
        bonus = 0
        if self.damage_class:
            plus_split = self.damage_class.split('+')
            if len(plus_split) == 2:
                bonus = int(plus_split[1])
            d_split = plus_split[0].split('D')
            min = int(d_split[0]) + bonus
            max = 6 * int(d_split[0]) + bonus
        return min, max

    def fix(self):
        self.damage_class = self.damage_class.upper()

        if self.meta_type.endswith(' Blaster'):
            self.caliber = 'n/a'
            min, max = self.get_damage_stats
            self.fusion_cell = f'{self.clip * min * max} trigs (FSC:{self.clip}^{min}x{max})'
            self.rof = 1
            self.tech_level = 7
            self.cost = 100 + (int(self.clip * min * max) / 100) * (10 + self.weapon_accuracy)
            self.rng = 30
        if self.meta_type.endswith(' Laser'):
            self.caliber = 'n/a'
            min, max = self.get_damage_stats
            self.fusion_cell = f'{self.clip * min * (max+2)} trigs (FSC:{self.clip}^{min}x{max + 2})'
            self.rof = 1
            self.cost = 80 + (int(self.clip * min * (max+2)) / 100) * (10 + self.weapon_accuracy)
            self.tech_level = 6
            self.rng = 30
        if self.meta_type.startswith('Medium '):
            self.rng *= 1.25
        elif self.meta_type.startswith('Heavy '):
            self.rng *= 1.5
        elif self.meta_type.startswith('Rifle '):
            self.rng *= 3
        elif self.meta_type.startswith('Shotgun '):
            self.rng *= 0.5
        if self.category == 'MELEE':
            self.tech_level = 4
            self.caliber = 'n/a'
            self.fusion_cell = 'n/a'
        if self.tech_level == 6:
            self.cost *= 2
        elif self.tech_level == 7:
            self.cost *= 3
        elif self.tech_level == 8:
            self.cost *= 10
        if self.meta_type == 'Rapier':
            self.conceilable = 'L'
        coeff = 1
        if self.rel == 'VR':
            coeff += 0.2
        elif self.rel == 'UR':
            coeff -= 0.2
        if self.availability == 'E':
            coeff -= 0.1
        elif self.availability == 'P':
            coeff += 0.2
        elif self.availability == 'R':
            coeff += 0.4
        if self.category != 'MELEE':
            self.cost = int(self.cost * coeff / 10) * 10

        self.get_stats_line()

    def get_stats_line(self):
        res = []
        res.append(self.reference)
        res.append(self.category)
        res.append('WA:' + str(self.weapon_accuracy))
        res.append(self.conceilable)
        res.append(self.availability)
        res.append('DC:' + self.damage_class)
        if self.category == 'MELEE':
            res.append('STR:' + str(self.str_min))
        else:
            res.append('Cal:' + self.caliber)
            res.append('ROF:' + str(self.rof))
            res.append('Clip:' + str(self.clip))
        res.append('RNG:' + str(self.rng))
        res.append(str(self.rel))
        res.append('£' + str(self.cost))
        self.stats = ' . '.join(res)  # ⦁⏺
        return self.stats

    def to_json(self):
        from collector.utils.basic import json_default
        jstr = json.loads(json.dumps(self, default=json_default, sort_keys=True, indent=4))
        return jstr


class Weapon(models.Model):
    from collector.models.character import Character
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    weapon_ref = models.ForeignKey(WeaponRef, on_delete=models.CASCADE)
    ammoes = models.PositiveIntegerField(default=0)
    weapon_of_choice = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return '%s=%s' % (self.character.full_name, self.weapon_ref.reference)


def refix(modeladmin, request, queryset):
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    for w in selected:
        WeaponRef.objects.get(pk=w).save()
    short_description = "Refix"


class WeaponRefAdmin(admin.ModelAdmin):
    list_display = (
        'reference', 'meta_type', 'origins', 'category', 'fusion_cell', 'caliber', 'clip', 'rng', 'weapon_accuracy',
        'damage_class','rof',
        'availability', 'cost', 'description')
    ordering = ('-category', 'meta_type', 'reference', 'origins', 'damage_class',)
    actions = [refix]
    list_filter = ['category', 'hidden', 'origins', 'caliber', 'meta_type', 'availability']
    search_fields = ['reference', 'origins', 'meta_type']


class WeaponCusto(models.Model):
    class Meta:
        ordering = ['character_custo', 'weapon_ref']

    from collector.models.character_custo import CharacterCusto
    character_custo = models.ForeignKey(CharacterCusto, on_delete=models.CASCADE)
    weapon_ref = models.ForeignKey(WeaponRef, on_delete=models.CASCADE)
    ammoes = models.PositiveIntegerField(default=0)
    weapon_of_choice = models.BooleanField(default=False, blank=True)


class WeaponInline(admin.TabularInline):
    model = Weapon


class WeaponCustoInline(admin.TabularInline):
    model = WeaponCusto
