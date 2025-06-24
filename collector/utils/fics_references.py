"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─

  (from Fading Suns CoreRulebook p91-92)
  Base AP..................: 60 AP -> 180 OP
  Base Skill OP............: 30 OP
  Everyman Skill OP .......: 20 OP
  Blessing/Curses..........: 10 OP
  Extra OP.................: 40 OP
  TOTAL ...................: 280 OP

  (review for FICS10: lifepath)
                                     AP SP DP BA BC OP
  Birthright........................ 12  0  0  0  0 36+
  Upbringing........................  5  5  0  0  0 20
  Apprenticeship....................  5  8  2  0  0 25
  Early Career...................... 10 10  5  3  0 48
  Tour of Duty (x2).................  2 10  4  0  0 20
  Worldly Benefits..................  0  0  0  7  0  7
"""

FONTSET = ['Cinzel', 'Trade+Winds', 'Imprima', 'Roboto', 'Philosopher', 'Ruda', 'Khand', 'Allura', 'Gochi+Hand',
           'Reggae+One', 'Syne+Mono', 'Zilla+Slab',"Ubuntu+Mono",  'Spartan', 'News+Cycle', 'Archivo', 'Francois+One', 'Caveat',
           'Gruppo', 'Voltaire', 'Kanit', "Fredericka+the+Great", 'Esteban', 'Pompiere', 'Niconne', 'Delius','Rationale',
           'Nanum+Pen+Script', 'Schoolbell', 'Jim+Nightshade', 'Estonia', 'East+Sea+Dokdo', 'Julee', 'Economica',
           'Anton', 'Long+Cang','Rationale',  'Birthstone', 'Condiment',"Metal+Mania",'Passero+One',"Mountains+of+Christmas","Shadows+Into+Light",'Anton+SC',"Gugi","Meddon"]


SOURCE_REFERENCES = (
    ('FS2CRB', "HDi Fading Suns Official"),
    ('FICS', "Zaffarelli Fading Suns"),
)

GROUPCHOICES = (
    ('AWA', "Awareness"),
    ('BOD', "Physical"),
    ('CON', "Control"),
    ('DIP', "Diplomacy"),
    ('EDU', "Education"),
    ('FIG', "Combat"),
    ('PER', "Performance"),
    ('SOC', "Social"),
    ('SPI', "Spirituality"),
    ('TIN', "Tinkering"),
    ('UND', "Underworld"),
    ('ITO', "Introspection"),
    ('ITE', "Interaction"),
)

DEGREE_GROUPS = (
    ('GENE', "Generic"),
    ('SECT', "Sects"),
    ('FOLO', "Forbidden Lore"),
    ('HOUS', "Houses"),
    ('GUIL', "Guilds"),
    ('POTM', "Privilege Of The Martyrs"),
    ('DOGM', "Dogma"),
    ('SYST', "Systems"),
    ('SPEC', "Species"),
    ('HOLD', "Householding"),
    ('UNDR', "Underworld"),
    ('MACA', "Magna Carta"),
    ('HUMA', "Humanities"),
)



SHORTCUTS = {
    "Academia": {
        'attribute': "PA_INT",
        'label': "INT + Academia",
        'rationale': "Show how knowledgeable you are",
    },
    "Observe": {
        'attribute': "PA_AWA",
        'label': "AWA + Observe",
        'rationale': "Remark a voice in a crowded soirée",
    },
    "Search": {
        'attribute': "PA_AWA",
        'label': "AWA + Search",
        'rationale': "Search an object dropped in a spacecraft",
    },
    "Inquiry": {
        'attribute': "PA_INT",
        'label': "INT + Inquiry",
        'rationale': "Deduce the windows of opportunity for a murder in a planning",
    },
    "Empathy": {
        'attribute': "PA_TEM",
        'label': "TEM + Empathy",
        'rationale': "Catch a strange behavior from someone",
    },
    "Riddles": {
        'attribute': "PA_INT",
        'label': "INT + Riddles",
        'rationale': "Fix a mathematical problem",
    },
    "Shoot": {
        'attribute': "PA_DEX",
        'label': "DEX + Shoot",
        'rationale': "Fire a ranged weapon",
    },
    "Melee": {
        'attribute': "PA_DEX",
        'label': "DEX + Melee",
        'rationale': "Block a thrust attack with your blade",
    },
    "Maneuver": {
        'attribute': "PA_DEX",
        'label': "DEX + Maneuver",
        'rationale': "Drive a mundane vehicle",
    },
    "Fight": {
        'attribute': "PA_AGI",
        'label': "AGI + Fight",
        'rationale': "Trip someone to the ground",
    },
    "Seduction/Persuasion": {
        'attribute': "PA_PRE",
        'label': "PRE + Seduction",
        'rationale': "Charm others",
    },
    "Etiquette": {
        'attribute': "PA_TEM",
        'label': "TEM + Etiquette",
        'rationale': "Mundane court conversation",
    },
    "Leadership": {
        'attribute': "PA_PRE",
        'label': "PRE + Leadership",
        'rationale': "Give orders to subsidiaries",
    },
    "Athletics": {
        'attribute': "PA_MOV",
        'label': "MOV + Athletics",
        'rationale': "Dodging",
    },

    "Bureaucracy": {
        'attribute': "PA_INT",
        'label': "INT + Bureaucracy",
        'rationale': "Fill shipment border transit documents",
    },
    "Focus": {
        'attribute': 'PA_WIL',
        'label': 'WIL + Focus',
        'rationale': "Keep focused on a task",
    },
    "Remedy": {
        'attribute': "PA_INT",
        'label': "INT + Remedy",
        'rationale': "Stabilize wounds",
    },
    "Gunnery": {
        'attribute': "PA_DEX",
        'label': "DEX + Gunnery",
        'rationale': "Heavy weapon fire",
    },
    "Knavery": {
        'attribute': "PA_PRE",
        'label': "PRE + Knavery",
        'rationale': "Convince someone with bullshit",
    },
    "Beastcraft": {
        'attribute': "PA_INT",
        'label': "PRE + Beastcraft",
        'rationale': "Calm a mount during storm",
    },
    "Redemption": {
        'attribute': "PA_TEC",
        'label': "TEC + Redemption",
        'rationale': "Fix something",
    },
    "Teaching": {
        'attribute': "PA_TEM",
        'label': "TEM + Teaching",
        'rationale': "Teach students",
    },
    "Impress": {
        'attribute': "PA_STR",
        'label': "STR + Impresse",
        'rationale': "Convince those punks who is in charge here",
    },
    "Alchemy": {
        'attribute': "PA_AWA",
        'label': "AWA + Alchemy",
        'rationale': "Notice poison type by smell",
    },
    "Adaptation": {
        'attribute': "PA_AWA",
        'label': "TEC + Adaptation",
        'rationale': "Interpret strange data on ship sensors",
    },
}

ATTACK_ROLLS = {
    'MELEE': {
        'attribute': 'PA_DEX',
        'skill': 'Melee',
    },
    'P': {
        'attribute': 'PA_DEX',
        'skill': 'Shoot',
    },
    'RIF': {
        'attribute': 'PA_DEX',
        'skill': 'Shoot',
    },
    'SMG': {
        'attribute': 'PA_DEX',
        'skill': 'Shoot',
    },
    'HVY': {
        'attribute': 'PA_DEX',
        'skill': 'Heavy Weapons',
    },
}


LIFEPATH_CATEGORY = (
    ('0', "Birthright"),
    ('10', "Upbringing"),
    ('20', "Apprenticeship"),
    ('30', "Early Career"),
    ('40', "Tour of Duty"),
    ('50', "Worldly Benefits"),
    ('60', "Nameless Kit"),
    ('70', "Build"),
    ('80', "Special"),
)

LIFEPATH_CASTE = (
    ('Nobility', "Nobility"),
    ('Church', "Church"),
    ('Guild', "Guild"),
    ('Alien', "Alien"),
    ('Other', "Other"),
    ('Freefolk', "Freefolk"),
    ('Think Machine', "Think Machine"),
    ('Caliphate (PO)', "Kurgan (Planetary Origin)"),
    ('Caliphate (E)', "Kurgan (Environment)"),
    ('Caliphate (U)', "Kurgan (Usun)"),
    ('Barbarian', "Barbarian"),
    ('Empire', "Empire"),
    ('Supernatural', "Supernatural"),
)

RANGE = (
    ("0", "Touch"),
    ("1", "Sight"),
    ("2", "Sensory"),
    ("3", "Distance"),
    ("4", "Self"),
)

DURATION = (
    ("0", "Instant"),
    ("1", "Temporary"),
    ("2", "Prolonged"),
    ("3", "Perpetual"),
)

OCCULT_ARTS = (
    ("0", "Psi"),
    ("1", "Theurgy"),
    ("2", "Symbiosis"),
    ("3", "Runecasting"),
)

DRAMA_SEATS = (
    ('11-foe', 'Foe'),
    ('10-enemy', 'Enemy'),
    ('09-lackey', 'Lackey'),
    ('08-antagonist', 'Antagonist'),
    ('07-opponent', 'Opponent'),
    ('06-neutral', 'Neutral'),
    ('05-partisan', 'Partisan'),
    ('04-protagonist', 'Protagonist'),
    ('03-servant', 'Servant'),
    ('02-ally', 'Ally'),
    ('01-friend', 'Friend'),
    ('00-players', 'Players'),
)

DRAMA_SEATS_COLORS = {
    '11-foe': "#D08030",
    '10-enemy': "#C08040",
    '09-lackey': "#B08050",
    '08-antagonist': "#A08060",
    '07-opponent': "#908070",
    '06-neutral': "#808080",
    '05-partisan': "#708090",
    '04-protagonist': "#6080A0",
    '03-servant': "#5080B0",
    '02-ally': "#4080C0",
    '01-friend': "#3080D0",
    '00-players': "#D080D0"
}

BLOKES = {
    'allies': ['05-partisan', '04-protagonist', '03-servant', '02-ally', '01-friend'],
    'foes': ['11-foe', '10-enemy', '09-lackey', '08-antagonist', '07-opponent'],
    'others': ['06-neutral']
}

FICS_VERSION = 10.3