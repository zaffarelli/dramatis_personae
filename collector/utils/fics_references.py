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

MAX_CHAR = 25
RELEASE = '2.3.2'

LIFEPATH_CATEGORY = (
    ('0', "Birthright"),
    ('5', "Balance"),
    ('10', "Upbringing"),
    ('20', "Apprenticeship"),
    ('30', "Early Career"),
    ('40', "Tour of Duty"),
    ('50', "Worldly Benefits"),
    ('60', "Nameless Kit"),
)

# ('6',"Birthright balance"),

LIFEPATH_CATEGORY_SHORT = {
    '0': "BR",
    '5': "BA",
    '10': "UB",
    '20': "AP",
    '30': "EC",
    '40': "TD",
    '50': "WB",
    '60': "NK",
}

LIFEPATH_CATEGORY_VAL = {
    '0': (118, 120,  124, 131, 136, 160, 240, 300, 390, ),
    '5': (0, 4, 9, 16, 20, 22, ),
    '10': (20, 5, 15, ),
    '20': (25, ),
    '30': (48, ),
    '40': (10, 20, 30, 40, 240, 300, ),
    '50': (7, ),
    '60': (70, ),
}

LIFEPATH_CASTE = (
    ('Nobility', "Nobility"),
    ('Church', "Church"),
    ('Guild', "Guild"),
    ('Alien', "Alien"),
    ('Other', "Other"),
    ('Freefolk', "Freefolk"),
)

LIFEPATH_CASTE_SHORT = {
    'Nobility': "Nob",
    'Church': "Chu",
    'Guild': "Gui",
    'Alien': "Ali",
    'Other': "Oth",
    'Freefolk': "Ffk",
}


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
#
# RACIAL_ATTRIBUTES = {
#     "ascorbite": {},
#     "etyri": {},
#     "gannok": {},
#     "hironem": {},
#     "kurgan": {},
#     "obuni": {
#         'PA_REF': 1,
#         'PA_AGI': 1,
#         'PA_STR': -1,
#         'PA_BOD': -1,
#         'PA_CON': -1,
#         'occult_level': 1
#     },
#     "oro'ym": {},
#     "ukari": {
#         'PA_REF': 1,
#         'PA_AGI': 1,
#         'PA_STR': -1,
#         'PA_BOD': -1,
#         'PA_CON': -1,
#         'PA_TEC': 1,
#         'occult_level': 1,
#         'occult_darkside': 1,
#     },
#     "urthish": {},
#     "symbiot": {},
#     "vau": {},
#     "vorox": {
#         'PA_STR': 2,
#         'PA_CON': 2,
#         'PA_BOD': 4,
#         'PA_INT': -1,
#         'PA_TEC': -2,
#         'PA_TEM': 1,
#     },
#     "vuldrok": {},
# }

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
        'rationale': "Fencing",
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
