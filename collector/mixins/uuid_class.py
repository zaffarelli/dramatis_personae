'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
import uuid

class UUIDClass(models.Model):
    class Meta:
        abstract = True

    uuid = models.UUIDField(null=True,blank=True,editable=False,unique=True)

    def fix(self):
        self.uuid = uuid.uuid3(uuid.NAMESPACE_DNS, f'{self.__class__.__name__}.{self}')
