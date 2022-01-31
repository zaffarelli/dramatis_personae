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
"""

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
)

SHORTCUTS = {
    "Observe": {
        'attribute': "PA_AWA",
        'label': "AWA + Observe",
        'rationale': "Notice something",
    },
    "Search": {
        'attribute': "PA_AWA",
        'label': "AWA + Search",
        'rationale': "Search a place",
    },
    "Inquiry": {
        'attribute': "PA_INT",
        'label': "INT + Inquiry",
        'rationale': "Deduce from data",
    },
    "Empathy": {
        'attribute': "PA_TEM",
        'label': "AWA + Empathy",
        'rationale': "Discern emotions",
    },
    "Dodge": {
        'attribute': "PA_AGI",
        'label': "AGI + Dodge",
        'rationale': "Avoid being hit",
    },
    "Shoot": {
        'attribute': "PA_REF",
        'label': "REF + Shoot",
        'rationale': "Fire a ranged weapon",
    },
    "Melee": {
        'attribute': "PA_REF",
        'label': "REF + Melee",
        'rationale': "Melee",
    },
    "Driving (Skycraft Piloting)": {
        'attribute': "PA_REF",
        'label': "REF + Driving (Skycraft Piloting)",
        'rationale': "Fly an aircraft",
    },
    "Driving (Celestial Sailing)": {
        'attribute': "PA_TEC",
        'label': "TEC + Driving (Celestial Sailing)",
        'rationale': "Sailing a spaceship",
    },
    "Fight": {
        'attribute': "PA_REF",
        'label': "REF + Fight",
        'rationale': "Fight/Martial Arts",
    },
    "Persuasion": {
        'attribute': "PA_PRE",
        'label': "PRE + Persuasion",
        'rationale': "Convince someone with arguments",
    },
    "Seduction": {
        'attribute': "PA_PRE",
        'label': "PRE + Seduction",
        'rationale': "Charm others",
    },
    "Leadership": {
        'attribute': "PA_PRE",
        'label': "PRE + Leadership",
        'rationale': "Give orders to subsidiaries",
    },
    "Athletics": {
        'attribute': "PA_BOD",
        'label': "BOD + Athletics",
        'rationale': "Swimming",
    },
    "Acrobatics": {
        'attribute': "PA_MOV",
        'label': "MOV + Acrobatics",
        'rationale': "Roll to cover",
    },
    "Bureaucracy": {
        'attribute': "PA_INT",
        'label': "INT + Bureaucracy",
        'rationale': "Fill shipment border transit documents",
    },
    "Stoic Mind": {
        'attribute': 'PA_WIL',
        'label': 'WIL + Stoic Mind',
        'rationale': "Iron will",
    },
    "Focus": {
        'attribute': 'PA_WIL',
        'label': 'WIL + Focus',
        'rationale': "Keep focused on a task",
    },
    "Surgery": {
        'attribute': "PA_INT",
        'label': "INT + Surgery",
        'rationale': "Apply surgery on wounded",
    },
    "Science (Cybernetics)": {
        'attribute': "PA_TEC",
        'label': "TEC + Cybernetics",
        'rationale': "Surgically implant cyber",
    },
    "Remedy": {
        'attribute': "PA_INT",
        'label': "INT + Remedy",
        'rationale': "Stabilize wounds",
    },
    "Heavy Weapons": {
        'attribute': "PA_REF",
        'label': "REF + Heavy Weapons",
        'rationale': "Heavy weapon fire",
    },
    "Knavery": {
        'attribute': "PA_PRE",
        'label': "PRE + Knavery",
        'rationale': "Convince someone with bullshit",
    },
    "Magna Carta": {
        'attribute': "PA_INT",
        'label': "INT + Magna Carta",
        'rationale': "Prepare a legal case",
    },
    "Redemption (Forbidden Lore)": {
        'attribute': "PA_TEC",
        'label': "TEC + Redemption (Forbidden Lore)",
        'rationale': "Fix Proscribed Technology",
    },
    "Science (Engineering)": {
        'attribute': "PA_TEC",
        'label': "TEC + Science (Engineering)",
        'rationale': "Maintain celestial ship propelers thrust",
    },
}

ATTACK_ROLLS = {
    'MELEE': {
        'attribute': 'PA_REF',
        'skill': 'Melee',
    },
    'P': {
        'attribute': 'PA_REF',
        'skill': 'Shoot',
    },
    'RIF': {
        'attribute': 'PA_REF',
        'skill': 'Shoot',
    },
    'SMG': {
        'attribute': 'PA_REF',
        'skill': 'Shoot',
    },
    'HVY': {
        'attribute': 'PA_REF',
        'skill': 'Heavy Weapons',
    },
}

FONTSET = ['Cinzel', 'Trade+Winds', 'Imprima', 'Roboto', 'Philosopher', 'Ruda', 'Khand', 'Allura', 'Gochi+Hand',
           'Reggae+One', 'Syne+Mono', 'Zilla+Slab', 'Spartan', 'News+Cycle', 'Archivo', 'Francois+One', 'Caveat',
           'Gruppo', 'Voltaire', "Fredericka+the+Great", 'Esteban', 'Pompiere', 'Niconne', 'Delius',
           'Nanum+Brush+Street', 'Schoolbell', 'Jim+Nightshade', 'Julee', 'Estonia']

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
