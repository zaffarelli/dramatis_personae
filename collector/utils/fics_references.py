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

MAX_CHAR = 20
RELEASE = '0.5.0'

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

FONTSET = ['Cinzel', 'Trade+Winds', 'Imprima', 'Roboto', 'Philosopher', 'Ruda', 'Khand', 'Allura', 'Gochi+Hand',
           'Reggae+One', 'Syne+Mono', 'Zilla+Slab', 'Spartan', 'News+Cycle', 'Archivo', 'Francois+One', 'Caveat', 'Gruppo', 'Voltaire', "Fredericka+the+Great", 'Esteban', 'Pompiere']