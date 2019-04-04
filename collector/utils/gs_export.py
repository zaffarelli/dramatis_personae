'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
 Fading Suns
 Fusion Interlock Custom System v7
 This file contains the export to Google SpreadSheet functions
'''
from django.conf import settings
from collector.models.characters import Character
import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials

def connect():
  cred_file = settings.STATIC_ROOT+'collector/creds.json'
  scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
  credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_file, scope) 
  client = gspread.authorize(credentials) 
  sheet = client.open('FSTest').sheet1
  return sheet


def update_gss():  
  sheet = connect()

  character_items = Character.objects.all().filter(is_public=True,epic=1).order_by('full_name')
  row = 1
  sheet.update_cell(row,1, 'Name')
  sheet.update_cell(row,2, 'Alliance')
  sheet.update_cell(row,3, 'Dead')
  sheet.update_cell(row,4, 'Player')
  sheet.update_cell(row,5, 'Rank')
  sheet.update_cell(row,6, 'Gender')
  sheet.update_cell(row,7, 'Species')
  sheet.update_cell(row,8, 'Caste')
  sheet.update_cell(row,9, 'Age')
  sheet.update_cell(row,10, 'Entrance')
  sheet.update_cell(row,11, 'Picture')
  sheet.update_cell(row,12, 'AlliancePicture')
  sheet.update_cell(row,15, 'REGISTERED_ID')
  row = 2
  for c in character_items:
    sheet.update_cell(row,1, c.full_name)
    if c.is_partial == False:
      sheet.update_cell(row,2, c.alliance)
      sheet.update_cell(row,3, c.is_dead)
      sheet.update_cell(row,4, c.player)
      sheet.update_cell(row,5, c.rank)
      sheet.update_cell(row,6, c.gender)
      sheet.update_cell(row,7, c.castspecies.species)
      sheet.update_cell(row,8, c.caste)
      sheet.update_cell(row,9, c.age)
      sheet.update_cell(row,10, c.entrance)
      sheet.update_cell(row,11, '')
      sheet.update_cell(row,12, '')
      sheet.update_cell(row,15, c.rid)
    row += 1
    if row%10 == 0:
      time.sleep(110)
      sheet = connect()

# AIzaSyBz1VVHVSYoTUMKSTYo87TYZP9mnAlVe64

#row = sheet.row_values(1) # first row
# sheet.update_cell(2, 3, 'Blue')
# https://docs.google.com/spreadsheets/d/13k-4YYQOiTyGngrfHVQuqGbKcUpxfMn_KU0wFAFH9QE/edit?usp=sharing
# dp-98-126@dramatis-personae-236522.iam.gserviceaccount.com


