#!/usr/bin/env python3

from PyPDF2 import PdfFileMerger
from os import listdir
from os.path import isfile, join
import datetime
d = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
print("Launching makedp... at %s"%d)
mypath = 'collector/pdf/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
pdfs = onlyfiles
merger = PdfFileMerger()
print("Opening... header")
merger.append(open('collector/___header.pdf', 'rb'))
pdfs.sort()
print(pdfs)
for pdf in pdfs:
  #print("Opening... %s"%(pdf))
  merger.append(open(mypath+pdf, 'rb'))
des = 'collector/pdfbooks/dp_%s.pdf'%d
with open(des, 'wb') as fout:
  merger.write(fout)
  print("Writing... %s"%(des))
