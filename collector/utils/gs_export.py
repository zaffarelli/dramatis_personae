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
from collector.models.characters import Character
from collector.utils import fs_fics7
from collector.utils.basic import logger
import gspread
import yaml
from oauth2client.service_account import ServiceAccountCredentials

def connect(options):
  cf = options['collector']['export']['google_spread_sheet']['credentials']
  cred_file = settings.STATIC_ROOT+cf
  scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
  credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_file, scope) 
  client = gspread.authorize(credentials) 
  return client

def connect_as_source(options):
  source_name = options['collector']['export']['google_spread_sheet']['source_name']
  tab = options['collector']['export']['google_spread_sheet']['tab']
  client = connect(options)
  sheet = client.open(source_name).worksheet(tab)
  return sheet

def connect_as_target(options):
  target_name = options['collector']['export']['google_spread_sheet']['target_name']
  tab = options['collector']['export']['google_spread_sheet']['tab']
  client = connect(options)  
  sheet = client.open(target_name).worksheet(tab)      
  return sheet

def update_gss():
  options = fs_fics7.get_options()
  if options:
    header_line = gss_review(options)
    gss_push(options,header_line)
  else:
    logger.error('Something wrong append with the options file (config.yml)')

def gss_review(options):
  header_line = []
  sheet = connect_as_source(options)
  matrix = sheet.get_all_values()
  for idx, row in enumerate(matrix):
    if idx>0:
      print('> %s '%(row[0]))
      rid = fs_fics7.find_rid(row[0])
      try:
        c = Character.objects.get(rid=rid)
      except:
        c = None
      if c:
        change = False
        if row[10] != c.picture:
          c.picture = row[10]
          change = True
        if row[11] != c.alliance_picture:
          c.alliance_picture = row[11]
          change = True
        if change:
          c.save()
          change = False
      else:
        print('> %s does not exists (%s)'%(row[0],rid))
    else:
      for i in range(13):
        header_line.append(row[i])  
  print('> Review done')
  return header_line
  
def gss_push(options,header_line):  
  sheet = connect_as_target(options) 
  character_items = Character.objects.all().filter(is_public=True,epic=1,player='').order_by('alliance','full_name')
  matrix = sheet.range('A1:M%d'%(len(character_items)+1))
  for i in range(13):
    matrix[i].value = header_line[i]
  u = 1
  idx = 1
  for c in character_items:
    if c.is_partial:
      if c.use_only_entrance:
        matrix[idx*13+0].value = 'subject #%d (%s)'%(u,c.entrance)
        u+=1
      else:
        matrix[idx*13+0].value = c.full_name
      matrix[idx*13+1].value = '?'
      matrix[idx*13+2].value = ''
      matrix[idx*13+3].value = ''
      matrix[idx*13+4].value = ''
      matrix[idx*13+5].value = c.gender      
      matrix[idx*13+6].value = ''
      matrix[idx*13+7].value = ''
      matrix[idx*13+8].value = ''
      matrix[idx*13+9].value = c.entrance
      matrix[idx*13+10].value = c.picture
      matrix[idx*13+11].value = c.alliance_picture
      if c.use_only_entrance:
        matrix[idx*13+12].value = ''
      else:
        matrix[idx*13+12].value = c.rid
    else:
      matrix[idx*13+0].value = c.full_name
      matrix[idx*13+1].value = c.alliance
      matrix[idx*13+2].value = 'X' if c.is_dead else ''
      matrix[idx*13+3].value = c.player
      matrix[idx*13+4].value = c.rank
      matrix[idx*13+5].value = c.gender
      matrix[idx*13+6].value = c.specie.species
      matrix[idx*13+7].value = c.caste
      matrix[idx*13+8].value = c.age
      matrix[idx*13+9].value = c.entrance
      matrix[idx*13+10].value = c.picture
      matrix[idx*13+11].value = c.alliance_picture
      matrix[idx*13+12].value = c.rid
    idx += 1
  sheet.clear()
  sheet.update_cells(matrix)
  print('> Push Done')


