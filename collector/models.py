from django.db import models
from datetime import datetime

class Character(models.Model):
	full_name = models.CharField(max_length=200)
	alliance = models.CharField(max_length=200, default='none')
	player = models.CharField(max_length=200, default='none')
	PA_STR = models.IntegerField(default=0)
	PA_CON = models.IntegerField(default=0)
	PA_BOD = models.IntegerField(default=0)
	PA_MOV = models.IntegerField(default=0)
	PA_INT = models.IntegerField(default=0)
	PA_WIL = models.IntegerField(default=0)
	PA_TEM = models.IntegerField(default=0)
	PA_PRE = models.IntegerField(default=0)
	PA_REF = models.IntegerField(default=0)
	PA_TEC = models.IntegerField(default=0)
	PA_AGI = models.IntegerField(default=0)
	PA_AWA = models.IntegerField(default=0)
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

	def compute_secondaries(self):
		SA_REC = PA_STR + PA_CON
		SA_STA = PA_BOD * 2
		SA_END = (PA_BOD + PA_STR) * 5
		SA_STU = PA_CON + PA_BOD
		SA_RES = PA_WIL + PA_PRE
		SA_DMG = PA_STR / 2 - 1
		SA_TOL = PA_TEM + PA_WIL
		SA_HUM = (PA_TEM + PA_WIL) * 5
		SA_PAS = PA_TEM + PA_AWA
		SA_WYR = PA_INT + PA_REF
		SA_SPD = PA_REF / 2
		SA_RUN = PA_MOV + PA_MOV

	def __str__(self):
		return '%s' % self.full_name

class SkillRef(models.Model):
	reference = models.CharField(max_length=200)


class Skill(models.Model):
	character = models.ForeignKey(Character, on_delete=models.CASCADE)
	skill_ref = models.ForeignKey(SkillRef, on_delete=models.CASCADE)
	value = models.IntegerField(default=0)
