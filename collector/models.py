from django.db import models

# Create your models here.
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
	pub_date = models.DateTimeField('Date published')

class SkillRef(models.Model):
	reference = models.CharField(max_length=200)

class Skill(models.Model):
	character = models.ForeignKey(Character, on_delete=models.CASCADE)
	skill_ref = models.ForeignKey(SkillRef, on_delete=models.CASCADE)
	value = models.IntegerField(default=0)

