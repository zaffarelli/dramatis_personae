'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
 Fading Suns
 Fusion Interlock Custom System v7
 This file contains the export to Google SpreadSheet functions
'''
from django.conf import settings
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def update_gss():  
  cred_file = settings.STATIC_ROOT+'collector/creds.json'
  #scope = ['https://spreadsheets.google.com/feeds']
  scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

  credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_file, scope) 
  client = gspread.authorize(credentials) 
  sheet = client.open('Fading Suns Tests').sheet1 # open sheet
  data = sheet.get_all_records()
  print('Is it working? %s'%(data))


# AIzaSyBz1VVHVSYoTUMKSTYo87TYZP9mnAlVe64

#row = sheet.row_values(1) # first row
# sheet.update_cell(2, 3, 'Blue')
# https://docs.google.com/spreadsheets/d/13k-4YYQOiTyGngrfHVQuqGbKcUpxfMn_KU0wFAFH9QE/edit?usp=sharing
# dp-98-126@dramatis-personae-236522.iam.gserviceaccount.com


