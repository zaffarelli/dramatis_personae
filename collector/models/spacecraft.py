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
    ('19', "Atmospheric Transporter"),
    ('20', "Jumptug"),
)

MINIMUM_SYSTEMS = [
    {'reference': 'Fusion Core', 'minimum': 1, 'performance_per_ship_size': 10},
    {'reference': 'Maneuver Jets', 'per_ship_size': 2, 'performance_per_ship_size': 2},
    {'reference': 'Piloting Console', 'per_ship_size': 1},
    {'reference': 'Engineer Console', 'minimum': 1, 'performance_per_ship_size': 1, 'only_if': 'has_jump_capability'},
    {'reference': 'Propulsion Engine', 'minimum': 1, 'performance_per_ship_size': 10, 'only_if': 'has_jump_capability'},
    {'reference': 'Energy Shields', 'performance_per_ship_size': 2},
    {'reference': 'Catering', 'performance_per_crew': 2, 'only_if': 'has_jump_capability'},
    {'reference': 'Grooming', 'performance_per_crew': 3, 'only_if': 'has_jump_capability'},
    {'reference': 'Think Machine', 'minimum': 1, 'performance_per_ship_size': 2},
]

SD_SIZE = 0
SD_DIM_LENGTH = 1
SD_DIM_WIDTH = 2
SD_DIM_HEIGHT = 3
SD_PTS = 4

SHIPS_DATA = [
    {
        'class': 'Fighter',
        'size_rating': 1,
        'length': 10,
        'width': 5,
        "height": 7,
        "structure_points": 20,
        'grade': 2
    },
    {
        'class': 'Shuttle',
        'size_rating': 1,
        'length': 10,
        'width': 5,
        "height": 7,
        "structure_points": 30,
        'grade': 0
    },
    {
        'class': 'Bomber',
        'size_rating': 2,
        'length': 20, 'width': 8,
        "height": 8,
        "structure_points": 40, 'grade': 2},
    {
        'class': 'Explorer', 'size_rating': 3, 'length': 30, 'width': 10, "height": 7, "structure_points": 90,
        'grade': 0},
    {
        'class': 'Raider',
        'size_rating': 3,
        'length': 35,
        'width': 12,
        "height": 10,
        "structure_points": 120,
        'grade': 0
    },{
        'class': 'Escort',
        'size_rating': 4,
        'length': 40,
        'width': 13,
        "height": 10,
        "structure_points": 150,
        'grade': 0
    },{
        'class': 'Corvette',
        'size_rating': 5,
        'length': 80,
        'width': 10,
        "height": 10,
        "structure_points": 200,
        'grade': 0
    },{
        'class': 'Jumptug', 'size_rating': 3, 'length': 40, 'width': 20, "height": 5, "structure_points": 120,
        'grade': 0},
    {
        'class': 'Frigate', 'size_rating': 6, 'length': 60, 'width': 20, "height": 15, "structure_points": 260,
        'grade': 1
    },
    {
        'class': 'Galliot', 'size_rating': 7, 'length': 70, 'width': 23, "height": 17, "structure_points": 300,
        'grade': 1
    },
    {
        'class': 'Fast Freighter', 'size_rating': 8, 'length': 65, 'width': 33, "height": 25, "structure_points": 340,
        'grade': 2
    },
    {
        'class': 'Small Freighter', 'size_rating': 10, 'length': 90, 'width': 38, "height": 30, "structure_points": 380,
        'grade': 2
    },
    {
        'class': 'Assault Lander', 'size_rating': 10, 'length': 100, 'width': 33, "height": 25, "structure_points": 400,
        'grade': 0
    },
    {
        'class': 'Destroyer', 'size_rating': 10, 'length': 100, 'width': 33, "height": 25, "structure_points": 400,
        'grade': 2
    },
    {
        'class': 'Carrier', 'size_rating': 12, 'length': 100, 'width': 33, "height": 25, "structure_points": 500,
        'grade': 2
    },
    {
        'class': 'Cruiser',
        'size_rating': 14,
        'length': 140, 'width': 47, "height": 35, "structure_points": 600,
        'grade': 2
    },
    {
        'class': 'Large Freighter',
        'size_rating': 15, 'length': 150, 'width': 40, "height": 38,
        "structure_points": 600,
        'grade': 2
    },
    {
        'class': 'Luxury Liner',
        'size_rating': 15, 'length': 140, 'width': 50, "height": 38, "structure_points": 1300,
        'grade': 2
    },
    {
        'class': 'Dreadnough',
        'size_rating': 25,
        'length': 250, 'width': 80,
        "height": 62,
        "structure_points": 1200,
        'grade': 2
    },
    {
        'class': 'Space Station',
        'size_rating': 25,
        'length': 250,
        'width': 80,
        "height": 62,
        "structure_points": 1200,
        'grade': 2
    }
]


class ShipSystem(models.Model):
    class Meta:
        verbose_name = "Spacecraft: Ship System"
        ordering = ['type', 'reference']

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
    firebirds = models.PositiveIntegerField(default=0)
    tactical_effects = models.CharField(max_length=64, default='n/a', blank=True)
    strategical_effects = models.CharField(max_length=64, default='n/a', blank=True)
    description = models.TextField(max_length=1024, blank=True, null=True)

    def __str__(self):
        return f"{self.reference} [ {self.type} ]"

    def matches(self, term):
        """ Check for matching words in reference """
        return term.lower() in self.reference.lower()

    def fix(self):
        if self.type == "n/a":
            self.type = "standard"
        self.type = self.type.title()
        if self.rating == 0:
            self.rating = 1
        if self.matches("Propulsion Engine"):
            self.firebirds = self.performance * 800
        elif self.matches("Auxiliary Fusion Core"):
            self.firebirds = self.performance * 1500
        elif self.matches("Fusion Core"):
            self.firebirds = self.performance * 500
        elif self.matches("Energy Shields"):
            self.firebirds = self.performance * 150
        elif self.matches("Jumpdrive"):
            self.firebirds = self.performance * 500
        elif self.matches("Sathra Damper"):
            self.firebirds = self.performance * 250
        elif self.matches("Vac Bags"):
            self.firebirds = self.performance * 20
        elif self.matches("VoidSuits"):
            self.firebirds = self.performance * 80
        elif self.matches("Think Machine"):
            self.firebirds = self.performance * 1000


class ShipRef(models.Model):
    """ Reference class for each Spacecraft. Matches the call to arm spacecrafts inventory.
    """

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
    size_rating = models.PositiveIntegerField(default=1, blank=True)

    has_jump_capability = models.BooleanField(default=True)

    cargo_internal = models.IntegerField(default=0)
    cargo_external = models.IntegerField(default=0)
    manoeuver_speed = models.IntegerField(default=0)
    supplies = models.IntegerField(default=0)
    armor = models.IntegerField(default=0)
    vitality = models.IntegerField(default=0)
    cost = models.IntegerField(default=0)

    structure_points = models.PositiveIntegerField(default=0)
    structure_points_used = models.PositiveIntegerField(default=0)
    firebirds = models.IntegerField(default=0)
    ship_status = models.CharField(max_length=30, choices=SHIP_STATUS, default='wip')

    cs_engine = models.IntegerField(default=0)
    cs_thrust = models.IntegerField(default=0)
    cs_bulk = models.IntegerField(default=0)
    cs_fusion_core = models.IntegerField(default=0)

    cs_sensors = models.IntegerField(default=0)
    cs_crew = models.IntegerField(default=0)
    cs_firepower = models.IntegerField(default=0)
    cs_think_machine = models.IntegerField(default=0)
    cs_battle_shields = models.IntegerField(default=0)

    cs_power_consumption = models.IntegerField(default=0)
    cs_power_stack = models.IntegerField(default=0)
    cs_power_peak = models.IntegerField(default=0)

    cs_maneuver = models.IntegerField(default=0)
    cs_scanners = models.IntegerField(default=0)

    cs_cargo = models.IntegerField(default=0)
    cs_autonomy = models.IntegerField(default=0)
    cs_storage_units = models.IntegerField(default=0)
    cs_life_support = models.IntegerField(default=0)

    cs_shields = models.IntegerField(default=0)
    cs_hull = models.IntegerField(default=0)
    cs_structure = models.IntegerField(default=0)

    cs_deflect = models.IntegerField(default=0)
    cs_soak = models.IntegerField(default=0)
    cs_damage = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.get_ship_class_display()} class {self.reference}"

    def ship_data(self):
        from collector.utils.basic import json_default
        import json
        jdata = json.dumps(self, default=json_default, sort_keys=True, indent=4)
        data = json.loads(jdata)
        data['class'] = self.get_ship_class_display()
        data['grade'] = self.get_ship_grade_display()
        data['dimensions'] = self.dimensions
        return data



    @property
    def dimensions(self):
        return "%dx%dx%d" % (self.dim_length, self.dim_width, self.dim_height)

    def fix(self):
        print(f'-> Fixing {self.reference}')
        self.ship_status = "combat_ready"
        self.firebirds = 0;
        self.cost = 0
        for j in SHIPS_DATA:
            if j['class'] == self.ship_class:
                self.size = j['size_rating']
                self.dim_length = j['length']
                self.dim_width = j['width']
                self.dim_height = j['height']
                self.structure_points = j['structure_points']

        is_ok = self.check_minimum_systems()
        if is_ok != 'ok':
            self.ship_status = is_ok
        else:
            print(" --> Minimum requirements met.")
            self.check_system_slots()
            self.compute_cinematic_system()

    def check_minimum_systems(self):
        """ Function validating minimum amounts and performance of the systems according to the ship size and crew size.
            Possible conditions markers : jump_capability
        """
        answer = 'ok'
        temp_crew = 0
        for slot in self.shipsystemslot_set.filter(shipsystem__reference='Harness'):
            temp_crew += slot.amount
        self.cs_crew = temp_crew
        print(f"Crew size: {self.cs_crew}!")
        for req in MINIMUM_SYSTEMS:
            condition_met = True
            if 'only_if' in req:
                condition_met = getattr(self, req['only_if']) == True
            total_amount = 0
            total_performance = 0
            needed_amount = 0
            needed_performance = 0
            if "per_ship_size" in req and condition_met:
                needed_amount += req["per_ship_size"] * self.size_rating
            if "minimum" in req and condition_met:
                needed_amount += req["minimum"]
            if "per_crew" in req and condition_met:
                needed_amount += req["per_crew"] * temp_crew
            if "performance_per_ship_size" in req and condition_met:
                needed_performance += req["performance_per_ship_size"] * self.size_rating
            if "performance_per_crew" in req and condition_met:
                needed_performance += req["performance_per_crew"] * temp_crew
            for slot in self.shipsystemslot_set.filter(shipsystem__reference=req["reference"]):
                if needed_amount > 0:
                    amount_value = slot.amount
                    if slot.shipsystem.is_symetrical:
                        amount_value *= 2
                    total_amount += amount_value
                if needed_performance > 0:
                    perf_value = slot.amount * slot.shipsystem.performance
                    if slot.shipsystem.is_symetrical:
                        perf_value *= 2
                    total_performance += perf_value
            if needed_amount > 0:
                if total_amount < needed_amount:
                    answer = "req_not_met"
                    print(
                        f' --> Error while checking {self.reference}, system {req["reference"]} total amount is {total_amount} on {needed_amount} ')
                else:
                    print(
                        f' --> {self.reference} system [{req["reference"]}] checked! (amount {total_amount} on {needed_amount}) ')
            if needed_performance > 0:
                if total_performance < needed_performance:
                    answer = "req_not_met"
                    print(
                        f' --> Error while checking {self.reference}, system {req["reference"]} total performance is {total_performance} on {needed_performance} ')
                else:
                    print(
                        f' --> {self.reference} system [{req["reference"]}] performance checked! ({total_performance} on {needed_performance}) ')
        return answer

    def check_system_slots(self):
        slots = self.shipsystemslot_set.all()
        for slot in slots:
            slot.save()
        self.cs_power_consumption = 0
        self.cs_power_stack = 0
        self.structure_points_used = 0
        self.firebirds = 0
        for slot in slots:
            if slot.shipsystem:
                self.structure_points_used += slot.structure_points
                self.cs_power_consumption += slot.power_consumption
                self.cs_power_stack += slot.power_stack
                self.firebirds += slot.firebirds

    def compute_cinematic_system(self):
        self.cs_thrust = self.cs_engine - self.cs_bulk
        self.cs_maneuver = (
                                   self.cs_thrust + self.cs_engine - self.cs_bulk + self.cs_battle_shields + self.cs_fusion_core) / 3
        self.cs_scan = (self.cs_sensors + self.cs_fusion_core + self.cs_think_machine) / 3
        self.cs_soak = (self.cs_bulk + self.cs_crew - self.cs_engine)
        self.cs_autonomy = (self.cs_fusion_core + self.cs_bulk - self.cs_engine)


class ShipSystemSlot(models.Model):
    class Meta:
        verbose_name = "Spacecraft: System Slot"

    shipref = models.ForeignKey(ShipRef, on_delete=models.CASCADE, blank=True, null=True)
    shipsystem = models.ForeignKey(ShipSystem, on_delete=models.CASCADE, blank=True)
    amount = models.PositiveIntegerField(default=1, blank=True)
    structure_points = models.PositiveIntegerField(default=1, blank=True)
    power_consumption = models.IntegerField(default=0, blank=True)
    power_stack = models.PositiveIntegerField(default=0, blank=True)
    firebirds = models.PositiveIntegerField(default=0, blank=True)

    def fix(self):
        if self.shipsystem:
            real_amount = self.amount
            if self.shipsystem.is_symetrical:
                real_amount = self.amount * 2
            self.structure_points = real_amount * self.shipsystem.structure_points
            self.power_consumption = real_amount * self.shipsystem.power_consumption
            self.power_stack = real_amount * self.shipsystem.power_stack
            self.firebirds = real_amount * self.shipsystem.firebirds

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
    # registration_system = models.ForeignKey(System, on_delete=models.SET_NULL, blank=True, null=True)
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
        print(data)
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
    ordering = ['reference', 'type']
    list_display = ['reference', 'type', 'free_category', 'structure_points',
                    'performance', 'rating', 'is_symetrical', 'is_continuous_usage',
                    'power_consumption', 'power_stack', 'description', 'firebirds']
    list_filter = ['free_category', 'reference']
    search_fields = ['reference', 'type', 'autonomy']
    actions = [mass_save, mass_duplicate]
    list_editable = ['performance', 'structure_points', 'is_symetrical', 'is_continuous_usage', 'rating',
                     'power_consumption', 'power_stack', 'firebirds']  # , 'type', 'free_category']


class ShipRefAdmin(admin.ModelAdmin):
    ordering = ['builder']
    list_display = ['reference', 'ship_class', 'builder', 'ship_grade', 'dimensions', 'structure_points',
                    'structure_points_used', 'firebirds', 'ship_status']
    list_filter = ['builder', 'ship_class']
    actions = [mass_save, mass_duplicate]
    inlines = [ShipSystemSlotInline, ]


class ShipSystemSlotAdmin(admin.ModelAdmin):
    ordering = ['shipref', 'shipsystem']
    list_display = ['shipsystem', 'amount', 'power_consumption', 'power_stack', 'firebirds']
    list_filter = ('shipref', 'shipsystem', 'shipsystem__free_category')
    actions = [mass_save, mass_duplicate]


class SpaceshipAdmin(admin.ModelAdmin):
    ordering = ['full_name']
    list_display = ('full_name', 'ship_ref', 'owner', 'flag', 'notes', 'is_available')
    list_editable = ['is_available']
