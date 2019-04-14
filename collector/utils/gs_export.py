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
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def connect(target):
  cred_file = settings.STATIC_ROOT+'collector/creds.json'
  scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
  credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_file, scope) 
  client = gspread.authorize(credentials) 
  sheet = client.open(target).worksheet('PNJs')
  return sheet

def update_gss():  
    header_line = gss_review('Fading Suns')
    gss_push('Fading Suns',header_line)
    print('> update done')

def gss_review(target):
  header_line = []
  sheet = connect(target)
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
  
def gss_push(target,header_line):  
  sheet = connect(target) 
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
      matrix[idx*13+6].value = c.castspecies.species
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

