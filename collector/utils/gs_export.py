'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
 Fading Suns
 Fusion Interlock Custom System v7
 This file contains the export to Google SpreadSheet functions

 Share with: dp-98-126@dramatis-personae-236522.iam.gserviceaccount.com
'''
from django.conf import settings
from collector.models.character import Character
from collector.utils import fs_fics7
from collector.utils.basic import logger
import gspread
from datetime import datetime
from collector.utils.fics_references import RELEASE
import yaml
from oauth2client.service_account import ServiceAccountCredentials

from cryptography.fernet import Fernet



COLS_AMOUNT = 13

 # key = Fernet.generate_key() #this is your "password"
KEY = b'WAXSue9RLeTPqgdvbfrj2e60Xk6PrRgx6jo-KV8JOIw='

def encrypt(str):
    cipher_suite = Fernet(KEY)
    encoded_text = cipher_suite.encrypt(str.encode('UTF-8'))
    return encoded_text



def decrypt(str):
    cipher_suite = Fernet(KEY)
    decoded_text = cipher_suite.decrypt(str.encode('UTF-8'))
    return decoded_text

def connect(options):
    logger.info("> Connecting")
    cf = options['collector']['export']['google_spread_sheet']['credentials']
    cred_file = settings.STATIC_ROOT+cf
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    logger.info("> Sending Credentials")
    credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_file, scope)
    client = gspread.authorize(credentials)
    return client

def connect_as_source(options):
    logger.info("> Connecting source")
    source_name = options['collector']['export']['google_spread_sheet']['source_name']
    tab = options['collector']['export']['google_spread_sheet']['tab']
    client = connect(options)
    sheet = client.open(source_name).worksheet(tab)
    return sheet

def connect_as_target(options):
    logger.info("> Connecting target")
    target_name = options['collector']['export']['google_spread_sheet']['target_name']
    tab = options['collector']['export']['google_spread_sheet']['tab']
    client = connect(options)
    sheet = client.open(target_name).worksheet(tab)
    return sheet

def update_abstract(options):
    logger.info('> Writting Abstract')
    target_name = options['collector']['export']['google_spread_sheet']['target_name']
    tab = options['collector']['export']['google_spread_sheet']['tab_abstract']
    client = connect(options)
    sheet = client.open(target_name).worksheet(tab)
    matrix = sheet.range('A1:B4')
    matrix[0].value = "Source"
    matrix[1].value = "Dramatis Personae (Collector)"
    matrix[2].value = "Version"
    matrix[3].value = RELEASE
    matrix[4].value = "Exportation Date"
    matrix[5].value = datetime.now().strftime("%Y-%m-%d %H:%M")
    sheet.clear()
    sheet.update_cells(matrix)


def update_gss():
    options = fs_fics7.get_options()
    if options:
        header_line = gss_review(options)
        gss_push(options,header_line)
    else:
        logger.error('Something wrong happened with the options file (config.yml)')

def gss_review(options):
    header_line = []
    sheet = connect_as_source(options)
    matrix = sheet.get_all_values()
    for idx, row in enumerate(matrix):
        if idx>0:
            logger.info('> %s '%(row[0]))
            #rid = fs_fics7.find_rid(row[0])
            rid = decrypt(row[12]).decode('UTF-8')
            logger.info('> %s '%(rid))
            try:
                c = Character.objects.get(rid=rid)
            except:
                c = None
            if c:
                change = False
                if row[2] == 'TRUE':
                    row[2] = True
                else:
                    row[2] = c.spotlight
                if row[3] == 'TRUE':
                    row[3] = True
                else:
                    row[3] = c.is_dead
                if row[2] != c.spotlight:
                    c.spotlight = row[2]
                    change = True
                if row[3] != c.is_dead:
                    c.is_dead = row[3]
                    change = True
                if row[10] != c.picture:
                    c.picture = row[10]
                    change = True
                if change:
                    c.save()
                    change = False
            else:
                logger.error('> %s does not exists (%s)'%(row[0],rid))
        else:
            for i in range(COLS_AMOUNT):
                header_line.append(row[i])
    logger.info('> Review done')
    return header_line

def gss_push(options,header_line):
    update_abstract(options)
    sheet = connect_as_target(options)
    character_items = Character.objects.all().filter(epic__shortcut='DEM',is_public=True).order_by('alliance','full_name')
    logger.info("There will be %d characters"%(len(character_items)))
    matrix = sheet.range('A1:M%d'%(len(character_items)+1))
    #logger.info(header_line)
    for i in range(COLS_AMOUNT):
        matrix[i].value = header_line[i]
    u = 1
    idx = 1
    for c in character_items:
        if c.is_partial:
            if c.use_only_entrance:
                matrix[idx*COLS_AMOUNT+0].value = 'subject #%d (%s)'%(u,c.entrance)
                u+=1
            else:
                matrix[idx*COLS_AMOUNT+0].value = c.full_name
            matrix[idx*COLS_AMOUNT+1].value = '?'
            matrix[idx*COLS_AMOUNT+2].value = c.spotlight
            matrix[idx*COLS_AMOUNT+3].value = c.is_dead
            matrix[idx*COLS_AMOUNT+4].value = ''
            matrix[idx*COLS_AMOUNT+5].value = ''
            matrix[idx*COLS_AMOUNT+6].value = c.gender
            matrix[idx*COLS_AMOUNT+7].value = ''
            matrix[idx*COLS_AMOUNT+8].value = ''
            matrix[idx*COLS_AMOUNT+9].value = c.entrance
            matrix[idx*COLS_AMOUNT+10].value = c.picture
            matrix[idx*COLS_AMOUNT+11].value = ''
            matrix[idx*COLS_AMOUNT+12].value = encrypt(c.rid).decode('UTF-8')
        else:
            matrix[idx*COLS_AMOUNT+0].value = c.full_name
            matrix[idx*COLS_AMOUNT+1].value = c.alliance
            matrix[idx*COLS_AMOUNT+2].value = c.spotlight
            matrix[idx*COLS_AMOUNT+3].value = c.is_dead
            matrix[idx*COLS_AMOUNT+4].value = c.player
            matrix[idx*COLS_AMOUNT+5].value = c.rank
            matrix[idx*COLS_AMOUNT+6].value = c.gender
            matrix[idx*COLS_AMOUNT+7].value = c.specie.species
            matrix[idx*COLS_AMOUNT+8].value = c.age
            matrix[idx*COLS_AMOUNT+9].value = c.entrance
            matrix[idx*COLS_AMOUNT+10].value = c.picture
            matrix[idx*COLS_AMOUNT+11].value = c.faction
            matrix[idx*COLS_AMOUNT+12].value = encrypt(c.rid).decode('UTF-8')
        idx += 1
    sheet.clear()
    sheet.update_cells(matrix)
    logger.info('> Push Done')
