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

SHIPSYSTEM_CATEGORIES = (
    ('0',"Engine"),
    ('1',"Jumpdrive"),
    ('2',"Shield"),
    ('3',"Sensor"),
    ('4',"Turret"),
    ('5',"Direct Fire Weapon"),
    ('6',"Indirect Fire Weapon"),
    ('7',"Miscellaneous"),
    ('8',"Transmissions"),
    ('9',"Crew"),
)

SHIP_GRADES = (
    ('0',"Lander"),
    ('1',"Atmosphere"),
    ('2',"Void"),
)

SHIP_STATUS = (
    ('wip',"Work In Progress"),
    ('combat_ready',"Combat Ready"),
    ('invalid_sections',"Invalid Sections"),
)

SHIP_ENGINES = (
    ('1',"Slow"),
    ('2',"Standard"),
    ('3',"Fast"),
)

SHIP_SHIELDS = (
    ('2',"2/2"),
    ('4',"4/4"),
    ('6',"6/6"),
    ('8',"8/8"),
    ('9',"9/9"),
    ('12',"12/12"),
)

SHIELD_EFFECT = (
    ('0',"shield negates"),
    ('1',"ignores shield"),
    ('2',"burn out"),
    ('3',"overpower"),
    ('4',"auto burn out"),
)

SYSTEM_SIZE = (
    ('0',"h"),
    ('1',"S"),
    ('2',"M"),
    ('3',"L"),
)

SHIP_SLOTS = (
    ("0","Fore"),
    ("1","Fore Port"),
    ("2","Port"),
    ("3","Aft Port"),
    ("4","Aft"),
    ("5","Aft Starboard"),
    ("6","Starboard"),
    ("7","Fore Starboard"),
)

SHIP_SECTIONS = (
    ("0", "Bridge"),
    ("1", "Maneuver"),
    ("2", "Gundeck"),
    ("3", "Engine Room"),
    ("4", "Marines Deck"),
    ("5", "Turret A"),
    ("6", "Turret B"),
    ("7", "Turret Z"),
    ("8", "Spinal Mount"),
    ("9", "Shieldbank"),
    ("10", "Troop Quarters"),
    ("11", "Battleshield"),
)

SLOT_NAMES = (
    "Fore",
    "Fore Port",
    "Port",
    "Aft Port",
    "Aft",
    "Aft Starboard",
    "Starboard",
    "Fore Starboard",
)


SECTION_NAMES = [
    "Bridge",
    "Maneuver",
    "Gundeck",
    "Engine Room",
    "Marines Deck",
    "Turret A",
    "Turret B",
    "Turret Z",
    "Spinal Mount",
    "Shieldbank",
    "Troop Quarters",
    "Battle Shield",
]


SHIP_CLASSES = (
    ('0',"Fighter"),
    ('1',"Shuttle"),
    ('2',"Bomber"),
    ('3',"Explorer"),
    ('4',"Raider"),
    ('5',"Escort"),
    ('6',"Frigate"),
    ('7',"Galliot"),
    ('8',"Fast Freighter"),
    ('9',"Small Freighter"),
    ('10',"Assault Lander"),
    ('11',"Destroyer"),
    ('12',"Cruiser"),
    ('13',"Large Freighter"),
    ('14',"Luxury Liner"),
    ('15',"Dreadnough"),
    ('16',"Carrier"),
)

SHIP_DATA = (
    #Size        Thrust Maneuver mini max turrer Marines Gundecks
    # S   Dims      T  M  mT  MT  Ma G
    (1,   10,5,7,   16,8,  0,  0,  0,2  ),  # Fighter
    (1,   10,5,7,   12,6,  0,  0,  0,0  ),  # Shuttle
    (2,   20,8,8,   12,6,  0,  0,  0,4  ),  # Bomber
    (3,   30,10,7,  12,6,  0,  1,  0,3  ),  # Explorer
    (4,   35,12,10, 10,6,  0,  1,  1,10  ),  # Raider
    (4,   40,13,10,  8,4,  0,  1,  2,15  ),  # Escort
    (6,   60,20,15,  6,4,  0,  2,  8,30 ),  # Frigate
    (7,   70,23,17,  8,4,  0,  2, 16,20 ),  # Galliot
    (8,   65,33,25,  8,4,  0,  0, 16,3  ),  # Fast Freighter
    (10,  90,38,30,  6,2,  0,  0,  0,6  ),  # Small Freighter
    (10, 100,33,25,  8,4,  0,  0, 10,20 ),  # Assault Lander
    (10, 100,33,25,  4,2,  2,  4, 10,50 ),  # Destroyer
    (14, 140,47,35,  2,2,  8,  8, 14,75 ),  # Cruiser
    (15, 150,40,38,  2,2,  0,  0,  0,6  ),  # Large Freighter
    (15, 140,50,38,  2,2,  0,  0,  0,6  ),  # Luxury Liner
    (25, 250,80,62,  2,2, 12, 12, 30,105 ),  # Dreadnough
    (10, 100,33,25,  4,2,  2,  4, 10,20 ),  # Carrier
)

class ShipSystem(models.Model):
    class Meta:
        verbose_name = "Spacecraft: Ship System"
    reference = models.CharField(max_length=64)
    category = models.CharField(max_length=20,choices=SHIPSYSTEM_CATEGORIES,default='Miscellaneous',blank=True)
    tech_level = models.IntegerField(default=0)
    structure_points = models.PositiveIntegerField(default=0)
    firebirds = models.IntegerField(default=0)
    #hard_points = models.IntegerField(default=0)
    damage = models.IntegerField(default=0)
    size = models.CharField(max_length=1,choices=SYSTEM_SIZE,default='h',blank=True)
    pts = models.FloatField(default=0.0)
    pts_per_rating = models.FloatField(default=0.0)
    range = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    firebirds_per_rating = models.IntegerField(default=0)
    shield_effects = models.CharField(max_length=20,choices=SHIELD_EFFECT,default='shield negates',blank=True)
    description = models.TextField(max_length=1024, blank=True, null=True)
    effect = models.TextField(max_length=1024, blank=True, null=True)
    def __str__(self):
        return "%s"%(self.reference)

class ShipRef(models.Model):
    class Meta:
        verbose_name = "Spacecraft: Ship Reference"
        ordering = ('builder','size_rating',)
    reference = models.CharField(max_length=64, unique=True)
    builder = models.CharField(max_length=64, default='')
    ship_class = models.CharField(max_length=30,choices=SHIP_CLASSES,default='Shuttle',blank=True)
    ship_grade = models.CharField(max_length=30,choices=SHIP_GRADES,default='Void',blank=True)
    ship_engines = models.CharField(max_length=30,choices=SHIP_ENGINES,default='Standard',blank=True)
    ship_shields = models.CharField(max_length=30,choices=SHIP_SHIELDS,default='2/2',blank=True)
    battle_shields = models.PositiveIntegerField(default=0)
    jump_capability = models.PositiveIntegerField(default=0)
    crew = models.PositiveIntegerField(default=0)
    crew_marines = models.PositiveIntegerField(default=0)
    crew_marauders = models.PositiveIntegerField(default=0)
    crew_pilots = models.PositiveIntegerField(default=0)
    crew_engineers = models.PositiveIntegerField(default=0)
    crew_gunners = models.PositiveIntegerField(default=0)
    crew_jetjockeys = models.PositiveIntegerField(default=0)
    bridge_min = models.PositiveIntegerField(default=0)
    thrust_speed = models.PositiveIntegerField(default=0)
    size_rating = models.PositiveIntegerField(default=0)
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
    pts = models.FloatField(default=0.0)
    firebirds = models.IntegerField(default=0)
    ship_status = models.CharField(max_length=30,choices=SHIP_STATUS,default='wip')
    @property
    def shipsize(self):
        return "%03d"%(self.size_rating)
    @property
    def installed_sections(self):
        lst = []
        for f in self.shipsection_set.all():
            lst.append("%s %s"%(SLOT_NAMES[int(f.slot)], SECTION_NAMES[int(f.section)]))
        return ", ".join(lst)
    @property
    def dimensions(self):
        return "%dx%dx%d"%(self.dim_length,self.dim_width,self.dim_height)
    def __str__(self):
        return "%s"%(self.reference)
    def fix(self):
        self.ship_status = "combat_ready"
        self.firebirds = 0;
        self.cost = 0
        klass = int(self.ship_class)
        self.size_rating = SHIP_DATA[klass][0]
        self.dim_length  = SHIP_DATA[klass][1]
        self.dim_width   = SHIP_DATA[klass][2]
        self.dim_height  = SHIP_DATA[klass][3]
        try:
            for i in [1,3,5,7]:
                CheckOrCreateSection("1",str(i),self)
            for i in [0,1,3,4,5,7]:
                CheckOrCreateSection("9",str(i),self)
        except:
            logger.info("Spaceship [%s]: Error creating automatic sections."%(self.reference))
            self.ship_status = "invalid_sections"
        # Shield
        self.firebirds += 3000*int(self.ship_shields)
        if self.ship_status == "combat_ready":
            try:
                # Sensors
                for section in self.shipsection_set.all():
                    for slot in section.shipsystemslot_set.all():
                        sy = slot.shipsystem
                        #if sy.category == "3" or sy.category == "9":
                        self.firebirds += sy.firebirds + sy.rating*sy.firebirds_per_rating
                for section in self.shipsection_set.all():
                    if section.section != "9":
                        self.cost += section.structure_points
            except:
                logger.info("Spaceship [%s] not yet fixable... Next save will do."%(self.reference))
                import sys
                print(sys.exc_info()[0])
                self.ship_status = "wip"
        # Cargo
        self.cargo_internal = 10*self.size_rating
        # Hull
        self.firebirds += 10000*self.size_rating
        # Vitality
        self.vitality = self.size_rating*10
@receiver(pre_save, sender=ShipRef, dispatch_uid='update_ship_ref')
def update_ship_ref(sender, instance, **kwargs):
    instance.fix()

class ShipSection(models.Model):
    class Meta:
        verbose_name = "Spacecraft: Ship Section"
    section = models.CharField(max_length=30,choices=SHIP_SECTIONS,blank=True,default='0',null=True)
    ship_ref = models.ForeignKey(ShipRef, on_delete=models.CASCADE,blank=True)
    slot = models.CharField(max_length=30,choices=SHIP_SLOTS,blank=True,default='1',null=True)
    structure_points = models.PositiveIntegerField(default=1)
    boarding_party_limit = models.PositiveIntegerField(default=1)
    links = models.ManyToManyField("self",blank=True)
    def __str__(self):
        return "%s %s [#%03d]"%(SLOT_NAMES[int(self.slot)],SECTION_NAMES[int(self.section)],self.ship_ref.id)
    @property
    def systems_installed(self):
        lst = {}
        str_lst = []
        for s in self.shipsystemslot_set.all():
            if not str(s) in lst.keys():
                lst[str(s)] = 1
            else:
                lst[str(s)] += 1
        for k in lst:
            str_lst.append("%dx%s"%(lst[k],k))
        return ", ".join(str_lst)
    @property
    def boarding_access(self):
        lst = []
        for s in self.links.all():
            lst.append(str(s))
        return ", ".join(lst)


class ShipSectionInline(admin.TabularInline):
    model = ShipSection

class ShipSystemSlot(models.Model):
    class Meta:
        verbose_name = "Spacecraft: System Slot"
    shipsection = models.ForeignKey(ShipSection, on_delete=models.CASCADE,blank=True, null=True)
    shipsystem = models.ForeignKey(ShipSystem,on_delete=models.CASCADE,blank=True)
    def __str__(self):
        return "%s in %s"%(self.shipsystem,self.shipsection)

class ShipSystemSlotInline(admin.TabularInline):
    model = ShipSystemSlot
    ordering = ('shipsection',)


class Spaceship(models.Model):
    class Meta:
        verbose_name = "Spacecraft: Ship"
    full_name = models.CharField(max_length=200)
    ship_ref = models.ForeignKey(ShipRef,on_delete=models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey(Character,on_delete=models.SET_NULL, blank=True, null=True)
    flag = models.CharField(max_length=128, default='', null=True, blank=True)
    def __str__(self):
        return "%s (%s)"%(self.full_name,self.flag)
    def d3_model(self):
        d3_model = {}
        d3_model['info'] = {}
        d3_model['sections'] = []
        d3_model['links'] = []
        for s in self.shipsections_set.all():
            s_data = {}
            s_data['id'] = s.id
            s_data['structure_points'] = s.structure_points
            s_data['boarding_access'] = s.boarding_access
            s_data['name'] = SECTION_NAMES[int(s.shipsection)]
            s_data['slot'] = SLOT_NAMES[int(s.slot)]
            d3_model['sections'].append(s_data)
        return d3_model



def CheckOrCreateSection(section_name,slot_index,ship_ref):
    found = ShipSection.objects.filter(section=section_name,slot=slot_index,ship_ref=ship_ref)
    if len(found)==0:
        new_section = ShipSection()
        new_section.ship_ref = ship_ref
        new_section.section = section_name
        new_section.slot = str(slot_index)
        if new_section.section == '9':
            new_section.boarding_party_limit = 0
        new_section.save()



# ADMIN ------------------------------------------------------------------------

class ShipSystemAdmin(admin.ModelAdmin):
    ordering = ['category','reference']
    list_display = ('reference','category','tech_level','size','structure_points','damage','rating','firebirds','firebirds_per_rating','range','shield_effects', 'pts', 'pts_per_rating')
    list_filter = ('category','size','shield_effects')

class ShipRefAdmin(admin.ModelAdmin):
    ordering = ['builder','size_rating']
    list_display = ('reference','ship_class','builder','size_rating','ship_grade','ship_engines','ship_shields','cargo_internal', 'dimensions','installed_sections','cost','vitality','firebirds','ship_status')
    list_filter = ('builder','ship_class')
    inlines = [ ShipSectionInline, ]

class ShipSectionAdmin(admin.ModelAdmin):
    ordering = ['ship_ref','slot','section']
    list_display = ('section','slot','ship_ref','structure_points','systems_installed','boarding_access','boarding_party_limit')
    list_filter = ('ship_ref','section','slot','structure_points')
    search_fields = ('systems_installed',)
    inlines = [ ShipSystemSlotInline, ]

class ShipSystemSlotAdmin(admin.ModelAdmin):
    ordering = ['shipsection','shipsystem']
    list_display = ('shipsystem','shipsection')
    list_filter = ('shipsection','shipsystem')

class SpaceshipAdmin(admin.ModelAdmin):
    ordering = ['full_name']
    list_display = ('full_name','ship_ref','owner','flag')
