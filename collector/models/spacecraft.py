"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from django.db import models
from collector.models.character import Character
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.contrib import admin
import logging

logger = logging.getLogger(__name__)

LIGHTSPEED_RATIO = 0.05

SHIP_GRADES = (
    ('0', "Lander"),
    ('1', "Atmospheric"),
    ('2', "Void"),
)

SHIP_STATUS = (
    ('wip', "Work In Progress"),
    ('combat_ready', "Combat Ready"),
    ('req_not_met', "Minimum Ship Requirements not Met"),
)

SHIP_CLASSES = (
    ('0', "Fighter"),
    ('1', "Shuttle"),
    ('2', "Bomber"),
    ('3', "Explorer"),
    ('4', "Raider"),
    ('5', "Escort"),
    ('6', "Corvette"),
    ('7', "Frigate"),
    ('8', "Galliot"),
    ('9', "Fast Freighter"),
    ('10', "Small Freighter"),
    ('11', "Assault Lander"),
    ('12', "Destroyer"),
    ('13', "Cruiser"),
    ('14', "Large Freighter"),
    ('15', "Luxury Liner"),
    ('16', "Dreadnough"),
    ('17', "Carrier"),
    ('18', "Space Station"),
)

MINIMUM_SYSTEMS = [
    {'reference': 'Fusion Core', 'per_ship_size': 10},
    {'reference': 'Maneuver Jets', 'per_ship_size': 2},
    {'reference': 'Piloting Console', 'per_ship_size': 1},
    {'reference': 'Propulsion Engine', 'per_ship_size': 5},
]

SD_SIZE = 0
SD_DIM_LENGTH = 1
SD_DIM_WIDTH = 2
SD_DIM_HEIGHT = 3

SHIPS_DATA = (
    # Size        Thrust Maneuver mini max turrer Marines Gundecks
    # S   Dims      T  M  mT  MT  Ma G
    (1, 10, 5, 7, 16, 8, 0, 0, 0, 2),  # Fighter
    (1, 10, 5, 7, 12, 6, 0, 0, 0, 0),  # Shuttle
    (2, 20, 8, 8, 12, 6, 0, 0, 0, 4),  # Bomber
    (3, 30, 10, 7, 12, 6, 0, 1, 0, 3),  # Explorer
    (4, 35, 12, 10, 10, 6, 0, 1, 1, 10),  # Raider
    (4, 40, 13, 10, 8, 4, 0, 1, 2, 15),  # Escort
    (5, 50, 20, 15, 8, 4, 0, 1, 2, 15),  # Corvette
    (6, 60, 20, 15, 6, 4, 0, 2, 8, 30),  # Frigate
    (7, 70, 23, 17, 8, 4, 0, 2, 16, 20),  # Galliot
    (8, 65, 33, 25, 8, 4, 0, 0, 16, 3),  # Fast Freighter
    (10, 90, 38, 30, 6, 2, 0, 0, 0, 6),  # Small Freighter
    (10, 100, 33, 25, 8, 4, 0, 0, 10, 20),  # Assault Lander
    (10, 100, 33, 25, 4, 2, 2, 4, 10, 50),  # Destroyer
    (14, 140, 47, 35, 2, 2, 8, 8, 14, 75),  # Cruiser
    (15, 150, 40, 38, 2, 2, 0, 0, 0, 6),  # Large Freighter
    (15, 140, 50, 38, 2, 2, 0, 0, 0, 6),  # Luxury Liner
    (25, 250, 80, 62, 2, 2, 12, 12, 30, 105),  # Dreadnough
    (10, 100, 33, 25, 4, 2, 2, 4, 10, 20),  # Carrier

)


class ShipSystem(models.Model):
    class Meta:
        verbose_name = "Spacecraft: Ship System"

    reference = models.CharField(max_length=64)
    type = models.CharField(max_length=64, default='standard')
    free_category = models.CharField(max_length=64, default='n/a', blank=True)
    # category = models.CharField(max_length=20, choices=SHIPSYSTEM_CATEGORIES, default='Miscellaneous', blank=True)
    tech_level = models.IntegerField(default=6)
    performance = models.IntegerField(default=1)
    range = models.IntegerField(default=0)
    rating = models.IntegerField(default=1)
    structure_points = models.PositiveIntegerField(default=1)
    power_consumption = models.IntegerField(default=10)
    power_stack = models.IntegerField(default=0)
    is_continuous_usage = models.BooleanField(default=True)
    is_symetrical = models.BooleanField(default=False)
    pancreator_irae = models.PositiveIntegerField(default=0)
    tactical_effects = models.CharField(max_length=64, default='n/a', blank=True)
    strategical_effects = models.CharField(max_length=64, default='n/a', blank=True)
    description = models.TextField(max_length=1024, blank=True, null=True)

    def __str__(self):
        return f"{self.reference} [ {self.type} ]"

    def fix(self):
        if self.type == "n/a":
            self.type = "standard"
        self.type = self.type.title()
        if self.structure_points == 0:
            self.structure_points = 1
        if self.rating == 0:
            self.rating = 1


class ShipRef(models.Model):
    class Meta:
        verbose_name = "Spacecraft: Ship Reference"
        ordering = ['builder']

    reference = models.CharField(max_length=64, unique=True)
    builder = models.CharField(max_length=64, default='')
    ship_class = models.CharField(max_length=30, choices=SHIP_CLASSES, default='Shuttle', blank=True)
    ship_grade = models.CharField(max_length=30, choices=SHIP_GRADES, default='Void', blank=True)

    dim_length = models.PositiveIntegerField(default=0)
    dim_width = models.PositiveIntegerField(default=0)
    dim_height = models.PositiveIntegerField(default=0)

    cargo_internal = models.IntegerField(default=0)
    cargo_external = models.IntegerField(default=0)
    manoeuver_speed = models.IntegerField(default=0)
    supplies = models.IntegerField(default=0)
    armor = models.IntegerField(default=0)
    vitality = models.IntegerField(default=0)
    cost = models.IntegerField(default=0)
    structure_points = models.PositiveIntegerField(default=0)
    structure_points_used = models.PositiveIntegerField(default=0)
    pts = models.FloatField(default=0.0)
    firebirds = models.IntegerField(default=0)
    ship_status = models.CharField(max_length=30, choices=SHIP_STATUS, default='wip')

    cs_cargo = models.IntegerField(default=0)
    cs_engine = models.IntegerField(default=0)
    cs_thrust = models.IntegerField(default=0)
    cs_bulk = models.IntegerField(default=0)
    cs_fusion_core = models.IntegerField(default=0)
    cs_sensors = models.IntegerField(default=0)
    cs_crew = models.IntegerField(default=0)
    cs_guns = models.IntegerField(default=0)
    cs_think_machine = models.IntegerField(default=0)
    cs_battle_shields = models.IntegerField(default=0)

    cs_maneuver = models.IntegerField(default=0)
    cs_scan = models.IntegerField(default=0)
    cs_soak = models.IntegerField(default=0)
    cs_attack = models.IntegerField(default=0)
    cs_autonomy = models.IntegerField(default=0)

    def __str__(self):
        return "%s" % (self.reference)


    def ship_data(self):
        data = {}
        data['model'] = self.reference
        data['class'] = self.get_ship_class_display()
        data['grade'] = self.get_ship_grade_display()
        data['builder'] = self.builder
        return data

    def compute_cinematic_system(self):
        self.cs_maneuver = (
                                   self.cs_thrust + self.cs_engine - self.cs_bulk + self.cs_battle_shields + self.cs_fusion_core) / 3
        self.cs_scan = (self.cs_sensors + self.cs_fusion_core + self.cs_think_machine) / 3
        self.cs_soak = (self.cs_bulk + self.cs_crew - self.cs_engine)
        self.cs_attack = (self.cs_guns + self.cs_engine) / 2
        self.cs_autonomy = (self.cs_fusion_core + self.cs_bulk - self.cs_engine)


    @property
    def dimensions(self):
        return "%dx%dx%d" % (self.dim_length, self.dim_width, self.dim_height)



    def fix(self):
        print(f'-> Fixing {self.reference}')
        self.ship_status = "combat_ready"
        self.firebirds = 0;
        self.cost = 0
        klass = int(self.ship_class)
        self.size_rating = SHIPS_DATA[klass][SD_SIZE]
        self.dim_length = SHIPS_DATA[klass][SD_DIM_LENGTH]
        self.dim_width = SHIPS_DATA[klass][SD_DIM_WIDTH]
        self.dim_height = SHIPS_DATA[klass][SD_DIM_HEIGHT]

        self.structure_points = self.dim_length * self.dim_width * self.dim_height / 100

        is_ok = self.check_minimum_systems()
        if is_ok != 'ok':
            self.ship_status = is_ok
        else:
            self.check_system_slots()

        # self.compute_cinematic_system()

    def check_system_slots(self):
        slots = self.shipsystemslot_set.all()
        self.structure_points_used = 0
        for slot in slots:
            if slot.shipsystem:
                self.structure_points_used += slot.amount * slot.shipsystem.structure_points

    def check_minimum_systems(self):
        answer = 'ok'
        for req in MINIMUM_SYSTEMS:
            total = 0
            needed = req["per_ship_size"] * self.size_rating
            for slot in self.shipsystemslot_set.filter(shipsystem__reference=req["reference"]):
                total += slot.amount * slot.shipsystem.performance
            if total < needed:
                logger.warning(f'While checking {self.reference}, system {req["reference"]} is {total} on {needed} ')
                answer = "req_not_met"
                print(f' -->While checking {self.reference}, system {req["reference"]} is {total} on {needed} ')
        return answer


class ShipSystemSlot(models.Model):
    class Meta:
        verbose_name = "Spacecraft: System Slot"

    shipref = models.ForeignKey(ShipRef, on_delete=models.CASCADE, blank=True, null=True)
    shipsystem = models.ForeignKey(ShipSystem, on_delete=models.CASCADE, blank=True)
    amount = models.PositiveIntegerField(default=1, blank=True)

    def __str__(self):
        return f"{self.shipsystem} x{self.amount} in {self.shipref}"


class ShipSystemSlotInline(admin.TabularInline):
    model = ShipSystemSlot


class Spaceship(models.Model):
    class Meta:
        verbose_name = "Spacecraft: Ship"

    from cartograph.models.system import System
    full_name = models.CharField(max_length=200)
    ship_ref = models.ForeignKey(ShipRef, on_delete=models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey(Character, on_delete=models.SET_NULL, blank=True, null=True)
    flag = models.CharField(max_length=128, default='', null=True, blank=True)
    registration_system = models.ForeignKey(System, on_delete=models.SET_NULL, blank=True, null=True)
    is_available = models.BooleanField(default=False)
    notes = models.TextField(max_length=512, default='', null=True, blank=True)
    video = models.CharField(max_length=128, default='', null=True, blank=True)

    def ship_data(self):
        data = {}
        data['full_name'] = self.full_name
        data['owner'] = self.owner.full_name
        data['flag'] = self.flag
        data['video'] = self.video
        data['registration_system'] = self.registration_system
        data['ref'] = self.ship_ref.ship_data()
        return data

    def __str__(self):
        return "%s (%s)" % (self.full_name, self.flag)






# ADMIN ------------------------------------------------------------------------
def mass_save(modeladmin, request, queryset):
    for ss in queryset:
        ss.save()
    short_description = "Save All"


def mass_duplicate(modeladmin, request, queryset):
    for ss in queryset:
        ss.pk = None
        ss.save()
    short_description = "Duplicate All"


class ShipSystemAdmin(admin.ModelAdmin):
    ordering = ['free_category', '-performance', 'reference']
    list_display = ['reference', 'type', 'free_category', 'structure_points',
                    'performance', 'rating', 'is_symetrical', 'is_continuous_usage',
                    'power_consumption', 'power_stack', 'description']
    list_filter = ['free_category']
    actions = [mass_save, mass_duplicate]
    list_editable = ['performance', 'structure_points', 'is_symetrical','is_continuous_usage', 'rating', 'power_consumption', 'power_stack']#, 'type', 'free_category']


class ShipRefAdmin(admin.ModelAdmin):
    ordering = ['builder']
    list_display = ['reference', 'ship_class', 'builder', 'ship_grade', 'dimensions', 'structure_points', 'structure_points_used','firebirds', 'ship_status']
    list_filter = ['builder', 'ship_class']
    actions = [mass_save, mass_duplicate]
    inlines = [ShipSystemSlotInline, ]


class ShipSystemSlotAdmin(admin.ModelAdmin):
    ordering = ['shipref', 'shipsystem']
    list_display = ('shipsystem',)
    list_filter = ('shipref', 'shipsystem')


class SpaceshipAdmin(admin.ModelAdmin):
    ordering = ['full_name']
    list_display = ('full_name', 'ship_ref', 'owner', 'flag', 'registration_system', 'notes', 'is_available')
    list_editable = ['is_available']
