from django.db import models
from datetime import datetime
from django.db.models.signals import pre_save
from django.dispatch import receiver
import hashlib
import math

class Character(models.Model):
	full_name = models.CharField(max_length=200)
	rid = models.CharField(max_length=200, default='none')
	alliance = models.CharField(max_length=200, default='none')
	player = models.CharField(max_length=200, default='none')
	species = models.CharField(max_length=200, default='urthish')
	birthdate = models.IntegerField(default=0)
	gender = models.CharField(max_length=30, default='male')
	native_fief = models.CharField(max_length=200, default='none')
	caste = models.CharField(max_length=100, default='Freefolk')
	rank = models.CharField(max_length=100, default='none')
	height = models.IntegerField(default=150)
	weight = models.IntegerField(default=50)
	narrative = models.TextField(default='...')
	PA_STR = models.IntegerField(default=3)
	PA_CON = models.IntegerField(default=3)
	PA_BOD = models.IntegerField(default=3)
	PA_MOV = models.IntegerField(default=3)
	PA_INT = models.IntegerField(default=3)
	PA_WIL = models.IntegerField(default=3)
	PA_TEM = models.IntegerField(default=3)
	PA_PRE = models.IntegerField(default=3)
	PA_REF = models.IntegerField(default=3)
	PA_TEC = models.IntegerField(default=3)
	PA_AGI = models.IntegerField(default=3)
	PA_AWA = models.IntegerField(default=3)
	pub_date = models.DateTimeField('Date published', default=datetime.now)
	SA_REC = models.IntegerField(default=0)
	SA_STA = models.IntegerField(default=0)
	SA_END = models.IntegerField(default=0)
	SA_STU = models.IntegerField(default=0)
	SA_RES = models.IntegerField(default=0)
	SA_DMG = models.IntegerField(default=0)
	SA_TOL = models.IntegerField(default=0)
	SA_HUM = models.IntegerField(default=0)
	SA_PAS = models.IntegerField(default=0)
	SA_WYR = models.IntegerField(default=0)
	SA_SPD = models.IntegerField(default=0)
	SA_RUN = models.IntegerField(default=0)
	PA_TOTAL = models.IntegerField(default=0)
	age = models.IntegerField(default=0)

	def compute_secondaries(self):
		# Rules revision 166
		self.rid = hashlib.sha224(bytes(self.full_name,'utf-8')).hexdigest()
		self.SA_REC = self.PA_STR + self.PA_CON
		self.SA_STA = math.ceil(self.PA_BOD / 2) - 1
		self.SA_END = (self.PA_BOD + self.PA_STR) * 5
		self.SA_STU = self.PA_CON + self.PA_BOD
		self.SA_RES = self.PA_WIL + self.PA_PRE
		self.SA_DMG = math.ceil(self.PA_STR / 2) - 2
		self.SA_TOL = self.PA_TEM + self.PA_WIL
		self.SA_HUM = (self.PA_TEM + self.PA_WIL) * 5
		self.SA_PAS = self.PA_TEM + self.PA_AWA
		self.SA_WYR = self.PA_INT + self.PA_REF
		self.SA_SPD = math.ceil(self.PA_REF / 2)
		self.SA_RUN = self.PA_MOV *2
		self.PA_TOTAL = self.PA_STR + self.PA_CON + self.PA_BOD + self.PA_MOV + self.PA_REF + self.PA_WIL + self.PA_AWA + self.PA_TEM + self.PA_AGI + self.PA_TEC + self.PA_PRE + self.PA_INT
		self.age = 5017 - self.birthdate

	def __str__(self):
		return '%s' % self.full_name


@receiver(pre_save, sender=Character, dispatch_uid="update_character")
def update_character(sender, instance, **kwargs):
	instance.compute_secondaries()
	print("%s --> %s" % (instance.full_name,instance.rid))


class SkillRef(models.Model):
	reference = models.CharField(max_length=200)
	def __str__(self):
		return '%s' % self.reference

class Skill(models.Model):
	character = models.ForeignKey(Character, on_delete=models.CASCADE)
	skill_ref = models.ForeignKey(SkillRef, on_delete=models.CASCADE)
	value = models.IntegerField(default=0)
	def __str__(self):
		return '%s=%s' % (self.character.full_name,self.skill_ref.reference)
