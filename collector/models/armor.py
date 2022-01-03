"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from django.db import models
from collector.models.character import Character
from django.contrib import admin
import json


class ArmorRef(models.Model):
    class Meta:
        ordering = ['reference']
        verbose_name = "FICS: Armor"

    reference = models.CharField(max_length=64, default='', unique=True)
    category = models.CharField(max_length=6,
                                choices=(('Soft', "Soft Armor"), ('Medium', "Medium Armor"), ('Hard', "Hard Armor")),
                                default='Soft')
    head = models.BooleanField(default=False)
    torso = models.BooleanField(default=True)
    left_arm = models.BooleanField(default=True)
    right_arm = models.BooleanField(default=True)
    left_leg = models.BooleanField(default=False)
    right_leg = models.BooleanField(default=False)
    stopping_power = models.PositiveIntegerField(default=2)

    material_fabric = models.BooleanField(default=False, verbose_name='FA')
    material_leather = models.BooleanField(default=False, verbose_name='LE')
    material_metal = models.BooleanField(default=False, verbose_name='ME')
    material_plastic = models.BooleanField(default=False, verbose_name='PL')
    material_synth = models.BooleanField(default=False, verbose_name='SY')
    material_ceramsteel = models.BooleanField(default=False, verbose_name='CE')
    material_reinforced = models.BooleanField(default=False, verbose_name='RE')
    material_light = models.BooleanField(default=False, verbose_name='LI')
    material_powered = models.BooleanField(default=False, verbose_name='PO')
    material_connected = models.BooleanField(default=False, verbose_name='CO')
    material_void = models.BooleanField(default=False, verbose_name='VO')

    he_sp = models.IntegerField(default=0, verbose_name='HE')
    to_sp = models.IntegerField(default=0, verbose_name='TO')
    wa_sp = models.IntegerField(default=0, verbose_name='WA')
    sa_sp = models.IntegerField(default=0, verbose_name='SA')
    wl_sp = models.IntegerField(default=0, verbose_name='WL')
    sl_sp = models.IntegerField(default=0, verbose_name='SL')

    cost = models.PositiveIntegerField(default=2)
    price = models.PositiveIntegerField(default=0)
    encumbrance = models.PositiveIntegerField(default=0, verbose_name='ENC')
    obstruction = models.PositiveIntegerField(default=0, verbose_name='OBS')
    meta_type = models.CharField(max_length=64, default='', blank=True)
    origins = models.CharField(max_length=64, default='', blank=True)
    tech_level = models.PositiveIntegerField(default=3, verbose_name='TL')
    description = models.TextField(max_length=1024, default='', blank=True)

    def fix(self):
        self.price = 0
        self.price = (self.he_sp + self.to_sp + self.wa_sp + self.sa_sp + self.wl_sp + self.sl_sp) * 1
        self.price -= self.encumbrance
        self.price -= self.obstruction
        print(self.price)
        coeffs = 0;
        if self.material_fabric:
            self.price *= 2
        if self.material_leather:
            self.price *= 3
        if self.material_metal:
            self.price *= 5
        if self.material_plastic:
            self.price *= 10
        if self.material_synth:
            self.price *= 12
        if self.material_ceramsteel:
            self.price *= 20
        if self.material_reinforced:
            coeffs += 40
        if self.material_light:
            coeffs += 50
        if self.material_powered:
            coeffs += 30
        if self.material_connected:
            coeffs += 50
        if self.material_void:
            coeffs += 200
        self.price *= 1 + coeffs / 10

    def __str__(self):
        return '%s - %s, SP:%s' % (self.category, self.reference, self.stopping_power)

    def to_json(self):
        from collector.utils.basic import json_default
        jstr = json.loads(json.dumps(self, default=json_default, sort_keys=True, indent=4))
        return jstr


class Armor(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    armor_ref = models.ForeignKey(ArmorRef, on_delete=models.CASCADE)

    def __str__(self):
        return '%s=%s' % (self.character.full_name, self.armor_ref.reference)


class ArmorCusto(models.Model):
    class Meta:
        ordering = ['character_custo', 'armor_ref']

    from collector.models.character_custo import CharacterCusto
    character_custo = models.ForeignKey(CharacterCusto, on_delete=models.CASCADE)
    armor_ref = models.ForeignKey(ArmorRef, on_delete=models.CASCADE)


class ArmorRefAdmin(admin.ModelAdmin):
    ordering = ['-price', '-category', 'tech_level', 'encumbrance', 'reference']
    list_display = ['reference', 'meta_type', 'origins', 'category', 'encumbrance', 'obstruction', 'he_sp', 'to_sp',
                    'sa_sp', 'wa_sp', 'sl_sp', 'wl_sp', 'cost', 'price', 'tech_level', 'material_fabric','material_leather',
                    'material_plastic', 'material_metal', 'material_synth', 'material_ceramsteel', 'material_reinforced', 'material_light',
                    'material_powered', 'material_connected', 'material_void']
    list_filter = ['category', 'origins', 'meta_type']
    search_fields = ['reference', 'meta_type', 'category']


class ArmorInline(admin.TabularInline):
    model = Armor


class ArmorCustoInline(admin.TabularInline):
    model = ArmorCusto
