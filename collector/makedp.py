# ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
#  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
# ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
#!/usr/bin/env python3

from PyPDF2 import PdfFileMerger
from os import listdir
from os.path import isfile, join
from django.conf import settings
import datetime

d = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
print('Launching makedp... at %s'%d)
mypath = 'media/pdf/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
pdfs = onlyfiles
merger = PdfFileMerger()
print('Opening... header')
merger.append(open('collector/___header.pdf', 'rb'))
pdfs.sort()
i = 0
for pdf in pdfs:
  #print("Opening... %s"%(pdf))
  if '0000_' in pdf:
    print('Skipping 0000_ file %s'%(pdf))
  else:
    i += 1
    merger.append(open(mypath+pdf, 'rb'))
if i>0:
  des = 'static/pdf/dp_%s.pdf'%d
  with open(des, 'wb') as fout:
    merger.write(fout)
    print('Writing... %s (%d characters)'%(des,i))
print('No data to catalog.')
