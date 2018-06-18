from openpyxl import Workbook
from openpyxl.compat import range
from openpyxl.utils import get_column_letter
from collector.models import Character,WeaponRef
from datetime import datetime 
from collector.fs_fics7 import minmax_from_dc


def export_header(ws,data):
  r = 2
  for num,d in enumerate(data,start=1):
    ws.cell(column=num, row=r, value=data[d]['title'])
    ws.column_dimensions[get_column_letter(num)].width = data[d]['width']

def export_row(ws, data, ch, r):
  for num,d in enumerate(data,start=1):
    ws.cell(column=num, row=r, value='%s'%(getattr(ch,data[d]['attribute'])))
    
def export_to_xls(filename='dramatis_personae.xls'):
  """ XLS extraction of the Characters """
  wb = Workbook()
  dest_filename = filename
  ws = wb.active
  # Abstract
  ws.title = 'Abstract'
  ws.column_dimensions['A'].width = 40
  ws.column_dimensions['B'].width = 30
  ws.cell(column=1, row=2, value='Source')
  ws.cell(column=2, row=2, value='Dramatis Personae Collector')
  ws.cell(column=1, row=3, value='Version')
  ws.cell(column=2, row=3, value='0.5')
  ws.cell(column=1, row=4, value='Release date')
  ws.cell(column=2, row=4, value='%s'%(datetime.now()))
  # Characters
  ws = wb.create_sheet('Characters')
  h = {
    '1':{'title':'Name','attribute':'full_name','width':40},
    '2':{'title':'RID','attribute':'rid','width':30},
    '3':{'title':'Entrance','attribute':'entrance','width':40},
    '4':{'title':'Alliance','attribute':'alliance','width':40},
    '5':{'title':'Rank','attribute':'rank','width':30},
    '6':{'title':'Gender','attribute':'gender','width':10},
    '7':{'title':'Species/Race','attribute':'species','width':20},
    '8':{'title':'Caste','attribute':'caste','width':30},
    '9':{'title':'Birthdate','attribute':'birthdate','width':10},
    '10':{'title':'Height','attribute':'height','width':10},
    '11':{'title':'Weight','attribute':'weight','width':10},
    '12':{'title':'STR','attribute':'PA_STR','width':10},
    '13':{'title':'CON','attribute':'PA_CON','width':10},
    '14':{'title':'BOD','attribute':'PA_BOD','width':10},
    '15':{'title':'MOV','attribute':'PA_MOV','width':10},
    '16':{'title':'INT','attribute':'PA_INT','width':10},
    '17':{'title':'WIL','attribute':'PA_WIL','width':10},
    '18':{'title':'TEM','attribute':'PA_TEM','width':10},
    '19':{'title':'PRE','attribute':'PA_PRE','width':10},
    '20':{'title':'TEC','attribute':'PA_TEC','width':10},
    '21':{'title':'REF','attribute':'PA_REF','width':10},
    '22':{'title':'AGI','attribute':'PA_AGI','width':10},
    '23':{'title':'AWA', 'attribute':'PA_AWA','width':10},
  }  
  ws.cell(column=1, row=1, value='Dramatis Personae')
  character_items = Character.objects.all().order_by('full_name')
  export_header(ws,h)
  cnt = 3
  for c in character_items:
    export_row(ws,h,c,cnt)
    cnt += 1

  # Weapons
  ws = wb.create_sheet('Weapons')
  h = {
    '1':{'title':'Ref','attribute':'reference','width':40},
    '2':{'title':'Cat','attribute':'category','width':10},
    '3':{'title':'WA','attribute':'weapon_accuracy','width':5},
    '4':{'title':'CO','attribute':'conceilable','width':5},
    '5':{'title':'AV','attribute':'availability','width':5},
    '6':{'title':'DC','attribute':'damage_class','width':15},
    '7':{'title':'cal.','attribute':'caliber','width':15},    
    '8':{'title':'STR','attribute':'str_min','width':5},
    '9':{'title':'RoF','attribute':'rof','width':5},
    '10':{'title':'Clip','attribute':'clip','width':5},
    '11':{'title':'RNG','attribute':'rng','width':5},
    '12':{'title':'RE','attribute':'rel','width':5},
    '13':{'title':'Cost','attribute':'cost','width':10},
    '14':{'title':'Description','attribute':'description','width':40},
  }
  ws.cell(column=1, row=1, value='Dramatis Personae')
  weaponref_items = WeaponRef.objects.all().order_by('category','damage_class')
  export_header(ws,h)
  cnt = 3
  for c in weaponref_items:
    export_row(ws,h,c,cnt)
    cnt += 1

  # And save everything
  wb.save(filename = dest_filename)
