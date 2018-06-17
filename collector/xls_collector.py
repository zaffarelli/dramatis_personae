from openpyxl import Workbook
from openpyxl.compat import range
from openpyxl.utils import get_column_letter
from collector.models import Character
from datetime import datetime 



def export_to_xls(filename='dramatis_personae.xls'):
  """ XLS extraction of the Characters """
  wb = Workbook()
  dest_filename = filename
  ws = wb.active
  ws.title = 'Abstract'

  ws.cell(column=1, row=2, value='Dramatis Personae')
  ws.cell(column=1, row=3, value='%s'%(datetime.now()))


  ws = wb.create_sheet('Characters')
  character_items = Character.objects.all().order_by('full_name')
  ws.cell(column=1, row=1, value='Dramatis Personae')
  cnt = 2
  ccc = 1
  ws.cell(column=ccc, row=cnt, value='Name')
  ws.column_dimensions['A'].width = 40
  ccc+=1
  ws.cell(column=ccc, row=cnt, value='RID')
  ws.column_dimensions['B'].width = 30
  ccc+=1
  ws.cell(column=ccc, row=cnt, value='Alliance')
  ws.column_dimensions['C'].width = 30
  ccc+=1
  ws.cell(column=ccc, row=cnt, value='Rank')
  ccc+=1
  ws.cell(column=ccc, row=cnt, value='Gender')
  ccc+=1
  ws.cell(column=ccc, row=cnt, value='Species/Race')
  ccc+=1
  ws.cell(column=ccc, row=cnt, value='Caste')
  ccc+=1
  ws.cell(column=ccc, row=cnt, value='Birthdate')
  ccc+=1
  ws.cell(column=ccc, row=cnt, value='Height')
  ccc+=1
  ws.cell(column=ccc, row=cnt, value='Weight')
  ccc+=1
  ws.cell(column=ccc, row=cnt, value='STR')
  ccc+=1
  ws.cell(column=ccc, row=cnt, value='CON')
  ccc+=1
  ws.cell(column=ccc, row=cnt, value='BOD')
  ccc+=1
  ws.cell(column=ccc, row=cnt, value='MOV')
  ccc+=1
  ws.cell(column=ccc, row=cnt, value='INT')
  ccc+=1
  ws.cell(column=ccc, row=cnt, value='WIL')
  ccc+=1
  ws.cell(column=ccc, row=cnt, value='TEM')
  ccc+=1
  ws.cell(column=ccc, row=cnt, value='PRE')
  ccc+=1
  ws.cell(column=ccc, row=cnt, value='TEC')
  ccc+=1
  ws.cell(column=ccc, row=cnt, value='REF')
  ccc+=1
  ws.cell(column=ccc, row=cnt, value='AGI')
  ccc+=1
  ws.cell(column=ccc, row=cnt, value='AWA')
  ccc+=1
  cnt = 3
  for c in character_items:
    ws.cell(column=1, row=cnt, value='%s'%(c.full_name))
    ws.cell(column=2, row=cnt, value='%s'%(c.rid))
    ws.cell(column=3, row=cnt, value='%s'%(c.alliance))
    ws.cell(column=4, row=cnt, value='%s'%(c.rank))
    ws.cell(column=5, row=cnt, value='%s'%(c.gender))
    ws.cell(column=6, row=cnt, value='%s'%(c.species))
    ws.cell(column=7, row=cnt, value='%s'%(c.caste))
    ws.cell(column=8, row=cnt, value='%s'%(c.birthdate))
    ws.cell(column=9, row=cnt, value='%s'%(c.height))
    ws.cell(column=10, row=cnt, value='%s'%(c.weight))
    ws.cell(column=11, row=cnt, value='%d'%(c.PA_STR))
    ws.cell(column=12, row=cnt, value='%d'%(c.PA_CON))
    ws.cell(column=13, row=cnt, value='%d'%(c.PA_BOD))
    ws.cell(column=14, row=cnt, value='%d'%(c.PA_MOV))
    ws.cell(column=15, row=cnt, value='%d'%(c.PA_INT))
    ws.cell(column=16, row=cnt, value='%d'%(c.PA_WIL))
    ws.cell(column=17, row=cnt, value='%d'%(c.PA_TEM))
    ws.cell(column=18, row=cnt, value='%d'%(c.PA_PRE))
    ws.cell(column=19, row=cnt, value='%d'%(c.PA_TEC))
    ws.cell(column=20, row=cnt, value='%d'%(c.PA_REF))
    ws.cell(column=21, row=cnt, value='%d'%(c.PA_AGI))
    ws.cell(column=22, row=cnt, value='%d'%(c.PA_AWA))
    cnt += 1
  wb.save(filename = dest_filename)
