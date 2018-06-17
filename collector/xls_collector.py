from openpyxl import Workbook
from openpyxl.compat import range
from openpyxl.utils import get_column_letter
from collector.models import Character,WeaponRef
from datetime import datetime 
from collector.fs_fics7 import minmax_from_dc


def export_header(ws,heads,colwidths):
  r = 2
  for num,h in enumerate(heads,start=0):
    ws.cell(column=num+1, row=r, value=h)
    ws.column_dimensions[get_column_letter(num+1)].width = colwidths[num]
    
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
  h = ['Name','RID','Entrance','Alliance','Rank','Gender','Species/Race','Caste','Birthdate','Height','Weight','STR','CON','BOD','MOV','INT','WIL','TEM','PRE','TEC','REF','AGI','AWA']
  w = [40,30,30,50,20,20,20,20,20,20,20,10,10,10,10,10,10,10,10,10,10,10,10]
  ws.cell(column=1, row=1, value='Dramatis Personae')
  character_items = Character.objects.all().order_by('full_name')
  export_header(ws,h,w)
  cnt = 3
  for c in character_items:
    x = 1
    ws.cell(column=x, row=cnt, value='%s'%(c.full_name))
    x += 1
    ws.cell(column=x, row=cnt, value='%s'%(c.rid))
    x += 1
    ws.cell(column=x, row=cnt, value='%s'%(c.entrance))
    x += 1
    ws.cell(column=x, row=cnt, value='%s'%(c.alliance))
    x += 1
    ws.cell(column=x, row=cnt, value='%s'%(c.rank))
    x += 1
    ws.cell(column=x, row=cnt, value='%s'%(c.gender))
    x += 1
    ws.cell(column=x, row=cnt, value='%s'%(c.species))
    x += 1
    ws.cell(column=x, row=cnt, value='%s'%(c.caste))
    x += 1
    ws.cell(column=x, row=cnt, value='%s'%(c.birthdate))
    x += 1
    ws.cell(column=x, row=cnt, value='%s'%(c.height))
    x += 1
    ws.cell(column=x, row=cnt, value='%s'%(c.weight))
    x += 1
    ws.cell(column=x, row=cnt, value='%d'%(c.PA_STR))
    x += 1
    ws.cell(column=x, row=cnt, value='%d'%(c.PA_CON))
    x += 1
    ws.cell(column=x, row=cnt, value='%d'%(c.PA_BOD))
    x += 1
    ws.cell(column=x, row=cnt, value='%d'%(c.PA_MOV))
    x += 1
    ws.cell(column=x, row=cnt, value='%d'%(c.PA_INT))
    x += 1
    ws.cell(column=x, row=cnt, value='%d'%(c.PA_WIL))
    x += 1
    ws.cell(column=x, row=cnt, value='%d'%(c.PA_TEM))
    x += 1
    ws.cell(column=x, row=cnt, value='%d'%(c.PA_PRE))
    x += 1
    ws.cell(column=x, row=cnt, value='%d'%(c.PA_TEC))
    x += 1
    ws.cell(column=x, row=cnt, value='%d'%(c.PA_REF))
    x += 1
    ws.cell(column=x, row=cnt, value='%d'%(c.PA_AGI))
    x += 1
    ws.cell(column=x, row=cnt, value='%d'%(c.PA_AWA))
    x += 1
    cnt += 1
  ws = wb.create_sheet('Weapons')
  h = ['Ref','Cat','WA','CO','AV','DC','cal.','MinMax','Str','RoF','Clip','RNG','RE','Cost','Description']
  w = [40,10,5,5,5,10,15,15,5,5,5,5,5,8,30]
  ws.cell(column=1, row=1, value='Dramatis Personae')
  weaponref_items = WeaponRef.objects.all().order_by('category','damage_class')
  export_header(ws,h,w)
  cnt = 3
  for c in weaponref_items:
    x = 1
    ws.cell(column=x, row=cnt, value='%s'%(c.reference))
    x += 1
    ws.cell(column=x, row=cnt, value='%s'%(c.category))
    x += 1
    ws.cell(column=x, row=cnt, value='%s'%(c.weapon_accuracy))
    x += 1
    ws.cell(column=x, row=cnt, value='%s'%(c.conceilable))
    x += 1
    ws.cell(column=x, row=cnt, value='%s'%(c.availability))
    x += 1
    ws.cell(column=x, row=cnt, value='%s'%(c.damage_class))
    x += 1
    ws.cell(column=x, row=cnt, value='%s'%(c.caliber))
    x += 1
    dcmm = minmax_from_dc(c.damage_class)
    ws.cell(column=x, row=cnt, value='%d-%d (%.02f)'%(dcmm[0],dcmm[1],((dcmm[0]+dcmm[1])/2)))
    x += 1
    ws.cell(column=x, row=cnt, value='%s'%(c.str_min))
    x += 1
    ws.cell(column=x, row=cnt, value='%s'%(c.rof))
    x += 1
    ws.cell(column=x, row=cnt, value='%s'%(c.clip))
    x += 1
    ws.cell(column=x, row=cnt, value='%s'%(c.rng))
    x += 1
    ws.cell(column=x, row=cnt, value='%s'%(c.rel))
    x += 1
    ws.cell(column=x, row=cnt, value='%s'%(c.cost))
    x += 1
    ws.cell(column=x, row=cnt, value='%s'%(c.description))
    x += 1
    cnt += 1
  wb.save(filename = dest_filename)
