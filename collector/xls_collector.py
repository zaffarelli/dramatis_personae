from openpyxl import Workbook
from openpyxl.compat import range
from openpyxl.utils import get_column_letter


def DramatisPersonaeToXsl(keyword, filename='dramatis_personae.xlsx'):
  wb = Workbook()
  dest_filename = filename
  ws = wb.create_sheet(title='Characters')
  character_items = Character.objects.filter('keyword='
  
  for row in range(10, 20):
    for col in range(27, 54):
      _= ws3.cell(column=col, row=row, value="{0}".format(get_column_letter(col)))

wb.save(filename = dest_filename)
