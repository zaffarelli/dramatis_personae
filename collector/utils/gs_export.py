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
import time
from oauth2client.service_account import ServiceAccountCredentials

def connect():
  cred_file = settings.STATIC_ROOT+'collector/creds.json'
  scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
  credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_file, scope) 
  client = gspread.authorize(credentials) 
  sheet = client.open('Fading Suns Tests').worksheet('PNJs')
  return sheet


def update_gss_old():  
  sheet = connect()
  matrix = sheet.get_all_values()
  character_items = Character.objects.all().filter(is_public=True,epic=1).order_by('full_name')
  matrix_final = sheet.range('A1:M95')  
  for idx, row in enumerate(matrix):
    if idx>0:
      rid = fs_fics7.find_rid(row[0])
      c = Character.objects.get(rid=rid)
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
        # Updating matrix
        if c.is_partial:
          row[0] = c.full_name
          row[1] = '?'
          row[2] = '?'
          row[3] = '?'
          row[4] = '?'
          row[5] = '?'
          row[6] = '?'
          row[7] = '?'
          row[8] = '?'
          row[9] = c.entrance
          row[10] = '?'
          row[11] = '?'
        else:
          row[1] = c.alliance
          row[2] = 'X' if c.is_dead else ''
          row[3] = c.player
          row[4] = c.rank
          row[5] = c.gender
          row[6] = c.castspecies.species
          row[7] = c.caste
          row[8] = c.age
          row[9] = c.entrance
          row[10] = c.picture
          row[11] = c.alliance_picture
        row[12] = c.rid
        print('%d) %s >> %s'%(idx,rid, c.full_name))       
      else:
        print('%d) /!\ Not found: %s'%(idx,rid))
      print(row)
    else:
      row[0] = 'Name'
      row[1] = 'Alliance'
      row[2] = 'Dead'
      row[3] = 'Player'
      row[4] = 'Rank'
      row[5] = 'Gender'
      row[6] = 'Species/Race'
      row[7] = 'Caste'
      row[8] = 'Age'
      row[9] = 'Entrance'
      row[10] = 'Picture'
      row[11] = 'AlliancePicture'
      row[12] = 'RID'      
      print('%d) (Header line)'%(idx))
    for i in range(13):
      cell = matrix_final[idx*13+i]
      cell.value = row[i]  
  sheet.update_cells(matrix_final)
  print('> Update Done')



def update_gss():  
  sheet = connect() 
  character_items = Character.objects.all().filter(is_public=True,epic=1,player='').order_by('use_only_entrance','full_name')
  matrix = sheet.range('A1:M%d'%(len(character_items)+1))  
  matrix[0].value = 'Name'
  matrix[1].value = 'Alliance'
  matrix[2].value = 'Dead'
  matrix[3].value = 'Player'
  matrix[4].value = 'Rank'
  matrix[5].value = 'Gender'
  matrix[6].value = 'Species/Race'
  matrix[7].value = 'Caste'
  matrix[8].value = 'Age'
  matrix[9].value = 'Entrance'
  matrix[10].value = 'Picture'
  matrix[11].value = 'AlliancePicture'
  matrix[12].value = 'RID'
  u = 1
  for idx, c in enumerate(character_items):
    if c.is_partial:
      if c.use_only_entrance:
        matrix[idx*13+0].value = 'subject #%d'%(u)
        u+=1
      else:
        matrix[idx*13+0].value = c.full_name
      matrix[idx*13+1].value = ''
      matrix[idx*13+2].value = ''
      matrix[idx*13+3].value = ''
      matrix[idx*13+4].value = ''
      if c.use_only_entrance:
        matrix[idx*13+5].value = c.gender      
      matrix[idx*13+6].value = ''
      matrix[idx*13+7].value = ''
      matrix[idx*13+8].value = ''
      matrix[idx*13+9].value = c.entrance
      matrix[idx*13+10].value = ''
      matrix[idx*13+11].value = ''
      matrix[idx*13+12].value = ''        
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
  sheet.clear()
  sheet.update_cells(matrix)
  print('> Brute push Done')


