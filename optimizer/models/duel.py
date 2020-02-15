'''
╔╦╗╔═╗  ╔═╗┌─┐┌┬┐┬┌┬┐┬┌─┐┌─┐┬─┐
 ║║╠═╝  ║ ║├─┘ │ │││││┌─┘├┤ ├┬┘
═╩╝╩    ╚═╝┴   ┴ ┴┴ ┴┴└─┘└─┘┴└─
'''
from django.db import models
from collector.models.character import Character
from datetime import datetime

class Duel(models.Model):
    pub_date = models.DateTimeField('Run date', default=datetime.now)
    tori = models.ForeignKey(Character, null=True, related_name='tori', on_delete=models.CASCADE)
    uke = models.ForeignKey(Character, null=True, related_name='uke', on_delete=models.CASCADE)
    type_of_fight = models.CharField(default="F2F",max_length=3, choices=[('F2F','Face to face'),('H2H','Hand to hand'),('MEL','MELEE'),('RNG','RANGED'),('MIX','MIXED')])
    rnd = 0

    @property
    def not_finished(self):
        someone_dead = (self.tori.check_death()) or (self.uke.check_death())
        return (self.rnd < 25) and not (someone_dead)

    def run(self):
        self.tori.hit_points = 40
        self.uke.hit_points = 40
        self.rnd = 0
        sequences = []
        while self.not_finished:
            self.rnd += 1
            round = CombatRound()
            round.run(self,self.rnd)
            sequences.append(round.round_summary)
        res = {'pub_date':self.pub_date,'rounds':sequences}
        return res

class CombatRound(models.Model):
    duel = models.ForeignKey(Duel, null=True, on_delete=models.CASCADE)
    attacker = models.ForeignKey(Character, null=True, related_name='attacker', on_delete=models.CASCADE)
    defender = models.ForeignKey(Character, null=True, related_name='defender', on_delete=models.CASCADE)
    number = models.PositiveIntegerField(default=0)
    round_summary = {}

    def run(self, duel, num):
        self.duel = duel
        self.number = num
        self.attacker = self.duel.uke
        self.defender = self.duel.tori
        self.round_summary = {}

        a,b = self.declaration_phase()
        c,d = self.initiative_phase()
        e,f = self.resolution_phase()

        self.round_summary['number'] = self.number
        self.round_summary['attacker'] = self.attacker.round_data
        self.round_summary['defender'] = self.defender.round_data
        self.round_summary['attacker']['hit_points'] = self.attacker.hit_points
        self.round_summary['defender']['hit_points'] = self.defender.hit_points
        # print("[1]\nA:%s \nD:%s"%(a,b))
        # print("[2]\nA:%s \nD:%s"%(c,d))
        # print("[3]\nA:%s \nD:%s"%(e,f))

    def declaration_phase(self):
        a = self.attacker.choose_attack()
        b = self.defender.choose_attack()
        return a,b

    def initiative_phase(self):
        a = self.attacker.initiative_roll()
        b = self.defender.initiative_roll()
        if self.attacker.round_data['Initiative'] <= self.defender.round_data['Initiative']:
            x = self.defender
            self.defender = self.attacker
            self.attacker = x
        return a,b

    def resolution_phase(self):
        a = self.attacker.roll_attack(self.defender)
        b = self.defender.absorb_punishment(self.attacker.round_data['damage'])
        if self.defender.check_death() == False:
            b = self.defender.roll_attack(self.attacker)
            a = self.attacker.absorb_punishment(self.defender.round_data['damage'])
        return a,b
