"""
    Dramatis Personae: Cartograph
"""
ORBITAL_ITEMS = (
    ('0', 'Sun'),
    ('1', 'Gas Giant'),
    ('2', 'Telluric'),
    ('3', 'Asteroids Belt'),
    ('4', 'Space Station'),
    ('5', 'Jumpgate'),
    ('6', 'Allied Forces'),
    ('7', 'Hostiles'),
)

NEW_ROUTES = [
    "Manitou_Icon",
    "Manitou_Cadiz",
    "Manitou_Vau",
    "Manitou_Apshai",
    "Vau_Vril Ya",
    "Cadiz_Vril Ya",
    "Apshai_Midian",
    "Apshai_Pandemonium",
    "Apshai_Rampart",
    "Vera Cruz_Hira",
    "Stigmata_Absolution",
    "Stigmata_Chernobog",
    "Stigmata_Daishan",
    "Absolution_Chernobog",
    "Chernobog_Daishan",
    "Absolution_Daishan",
    "Lemminkainen_Hargard",
    "Bannockburn_Verbannung_I",
    "Verona_Sunspear_II",
    "Grail_Verona_III",
    "Collier's Landing (Sargasso)_Rampart_IV",
    "Grail_Rimpoche_V",
    "Collier's Landing (Sargasso)_Eridol_VI",
    "Verona_Hira_VII",
    "Amena_Rhonda_VIII",
]

NEW_SYSTEMS = [
    "Hargard",
    "Verona",
    "Amena",
    "Apshai",
    "Manitou",
    "Vril Ya",
    "Vau",
    "Verbannung",
    "Rhonda",
    "Eridol",
    "Collier's Landing (Sargasso)",
    "Hira",
    "Absolution",
    "Chernobog",
    "Daishan",

]

BOOKS_DATA = [
    {
        "source": "Li Halan Fiefs",
        "name": "The Garden Worlds",
        "data": [
            {
                "system": "Kish",
                "jumproutes": ["Criticorum", "Icon", "Rampart", "Malignatus"],
                "ruler": "Prince Flavius Li Halan",
                "cathedral": "Zebulon's cathedral, Escoral (Orthodox)'",
                "agora": "Baahk Street, Escoral (Li Halan/Merchant League)",
                "garrison": 9,
                "capital": "Escoral",
                "jumps": 2,
                "solar_system": [
                    {"name": "Solasa", "category": "sun", "AU": 0.0},
                    {"name": "Akasha", "category": "telluric", "AU": 0.799},
                    {"name": "Kish", "category": "telluric", "AU": 0.935, "moons": ["Chira", "Rui"]},
                    {"name": "Vector", "category": "telluric", "AU": 3.015},
                    {"name": "Shatan", "category": "telluric", "AU": 9.235,
                     "moons": ["A", "B", "C", "D", "E", "F", "G"]},
                    {"name": "Urum", "category": "telluric", "AU": 19.010},
                    {"name": "Tern", "category": "telluric", "AU": 31.66},
                    {"name": "Jumpgate", "category": "jumpgate", "AU": 42.5}
                ],
                "tech": 6,
                "tech_complement": "4:or lower in rural areas",
                "population": {"human": 149, "alien": 1.5, "alien_note": "Mostly Obun, some Vorox"},
            },
            {
                "system": "Icon",
                "jumproutes": ["Kish", "Midian", "Ungavorox", "Manitou"],
                "ruler": "Grand Duke Maximino Li Halan",
                "cathedral": "Saint Lextius's cathedral, Bao (Orthodox)'",
                "agora": "Promonade, Bao (Merchant League)",
                "garrison": 5,
                "capital": "Bao",
                "jumps": 3,
                "solar_system": [
                    {"name": "Sun", "category": "sun", "AU": 0.0},
                    {"name": "Halo", "category": "telluric", "AU": 0.792},
                    {"name": "Icon", "category": "telluric", "AU": 1.0, "moons": ["Mandala"]},
                    {"name": "Conversion", "category": "telluric", "AU": 1.892},
                    {"name": "Angel's Reach", "category": "telluric", "AU": 5.097},
                    {"name": "Fatima", "category": "telluric", "AU": 16.037},
                    {"name": "Sophia", "category": "telluric", "AU": 27.370},
                    {"name": "Maria", "category": "telluric", "AU": 48.31},
                    {"name": "Tara", "category": "telluric", "AU": 59.87},
                    {"name": "Jumpgate", "category": "jumpgate", "AU": 72.3}
                ],
                "tech": 4,
                "tech_complement": "",
                "population": {"human": 512, "alien": 0.7, "alien_note": "Mainly Obun and Vorox, some Shantor"}
            },
            {
                "system": "Midian",
                "jumproutes": ["Leagueheim", "Icon", "Apshai"],
                "ruler": "Duke Augustus Zhu Li Halan",
                "cathedral": "Saint Palamedes cathedral, Santo Alecto (Orthodox)'",
                "agora": "Fu Street, Saiwuhn (Merchant League)",
                "garrison": 7,
                "capital": "Saiwuhn",
                "jumps": 3,
                "solar_system": [
                    {"name": "Xi-He", "category": "sun", "AU": 0.0},
                    {"name": "Fen-Hong", "category": "telluric", "AU": 0.265},
                    {"name": "Tai Bai", "category": "telluric", "AU": 0.423},
                    {"name": "Midian", "category": "telluric", "AU": 1.087, "moons": ["Peng-Lai"]},
                    {"name": "Lian", "category": "telluric", "AU": 3.864},
                    {"name": "Magyar", "category": "gaseous", "AU": 9.672},
                    {"name": "Kalevala", "category": "gaseous", "AU": 16.234},
                    {"name": "Jumpgate", "category": "jumpgate", "AU": 33.4}
                ],
                "tech": 4,
                "tech_complement": "6:in Lyonesse",
                "population": {"human": 670, "alien": 3, "alien_note": "Mainly Obun in Saiwuhn"}
            },
            {
                "system": "Rampart",
                "jumproutes": ["Kish", "Grail", "Apshai", "Pandemonium"],
                "ruler": "Countess Magu Li Halan",
                "cathedral": "Saint Paulus Cathedral, Avaneir (Orthodox)'",
                "agora": "The Metier (Independant guild)",
                "garrison": 8,
                "capital": "Avaneir",
                "jumps": 3,
                "solar_system": [
                    {"name": "Esperance", "category": "sun", "AU": 0.0},
                    {"name": "Rampart", "category": "telluric", "AU": 1.12, "moons": ["Chevalier"]},
                    {"name": "Devil's Belt", "category": "field", "AU": 3.267},
                    {"name": "Aeneas", "category": "telluric", "AU": 6.011},
                    {"name": "Tiers Monde", "category": "telluric", "AU": 9.003},
                    {"name": "Gargantua", "category": "gaseous", "AU": 16.207, "moons":["Draco","kraken"]},
                    {"name": "Lux", "category": "gaseous", "AU": 27.137},
                    {"name": "Kray's Watch", "category": "telluric", "AU": 42.33},
                    {"name": "Jumpgate", "category": "jumpgate", "AU": 62.33}
                ],
                "tech": 7,
                "tech_complement": "",
                "population": {"human": 423, "alien": 4, "alien_note": "Mainly Obun, Ukar and Etyri"},
                "source": "Li Halan Fiefs"
            },
            {
                "system": "Ungavorox",
                "jumproutes": ["Icon"],
                "ruler": "Grand Duke Maximino Li Halan",
                "cathedral": "Saint Lextius's cathedral, Bao (Orthodox)'",
                "agora": "Promonade, Bao (Merchant League)",
                "garrison": 5,
                "capital": "Bao",
                "jumps": 3,
                "solar_system": [
                    {"name": "Sun", "category": "sun", "AU": 0.0},
                    {"name": "Halo", "category": "telluric", "AU": 0.792},
                    {"name": "Icon", "category": "telluric", "AU": 1.0, "moons": ["Mandala"]},
                    {"name": "Conversion", "category": "telluric", "AU": 1.892},
                    {"name": "Angel's Reach", "category": "telluric", "AU": 5.097},
                    {"name": "Fatima", "category": "telluric", "AU": 16.037},
                    {"name": "Sophia", "category": "telluric", "AU": 27.370},
                    {"name": "Maria", "category": "telluric", "AU": 48.31},
                    {"name": "Tara", "category": "telluric", "AU": 59.87},
                    {"name": "Jumpgate", "category": "jumpgate", "AU": 72.3}
                ],
                "tech": 4,
                "tech_complement": "",
                "population": {"human": 512, "alien": 0.7, "alien_note": "Mainly Obun and Vorox, some Shantor"},
                "source": "Li Halan Fiefs"
            }
        ]
    }
]
