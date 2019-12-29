'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.apps import apps
from django.core.management.base import BaseCommand
from collector.models.fics_models import Role, Profile

roles = [         # PA Max Sk TA BA BC
  ['Legend',   8,   76,11, 70,0, 15,0],
  ['Champion', 7,   72,10, 60,0, 10,0],
  ['Elite',    6,   68,10, 55,0, 10,0],
  ['Veteran',  5,   64, 9, 50,0, 7, 0],
  ['Seasoned', 4,   60, 8, 45,0, 5, 0],
  ['Superior', 3,   56, 8, 40,0, 2, 0],
  ['Standard', 2,   52, 7, 35,0, 0, 0],
  ['Inferior', 1,   48, 7, 20,0, 0, 0],
  ['Undefined',0,    0,  0, 0, 0, 0, 0]
]

profiles = [  # Weights                   Groups
  ['physical', [3,3,3,3,1,1,1,1,1,1,1,1],['FIG','BOD']],
  ['spiritual',[1,1,1,1,3,3,3,3,1,1,1,1],['SOC','AWA']],
  ['tech',     [1,1,1,1,1,1,1,1,3,3,3,3],['TIN','CON','AWA']],
  ['courtisan',[3,3,3,3,3,3,3,3,1,1,1,1],['FIG','SOC','PER']],
  ['scholar',  [1,1,1,1,3,3,3,3,3,3,3,3],['EDU','SOC']],
  ['guilder',  [3,3,3,3,1,1,1,1,3,3,3,3],['FIG','TIN','CON']],
  ['standard', [1,1,1,1,1,1,1,1,1,1,1,1],[]]
]

class Command(BaseCommand):
  args = 'None'
  help = 'Populates the database with all the basic references.'

  @staticmethod
  def create(modname,data_list):
    #print('Inserting predefined data into the %s model...'%(modname))
    model = apps.get_model('collector',modname)
    fields = model._meta.fields
    fields_list = []
    for f in fields:
      fields_list.append(f.get_attname())
    fields_list.pop(0)
    for i in data_list:
      data_dict = dict(zip(fields_list,i)
      obj = model(**data_dict)
      obj.save()

  def handle(self, *args, **options):
    self.create('Role', roles)
    self.create('Profile', profiles)
