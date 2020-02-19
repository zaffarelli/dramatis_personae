'''
╔╦╗╔═╗  ╔═╗┌─┐┌┬┐┬┌┬┐┬┌─┐┌─┐┬─┐
 ║║╠═╝  ║ ║├─┘ │ │││││┌─┘├┤ ├┬┘
═╩╝╩    ╚═╝┴   ┴ ┴┴ ┴┴└─┘└─┘┴└─
'''
from django.db import models
from collector.models.character import Character
from datetime import datetime
import copy

class Duel:
    def __init__(self,tori,uke):
        self.tori = tori
        self.uke = uke
        self.rnd = 0
        self.pub_date = datetime.now()
        self.tori.prepare_for_battle()
        self.uke.prepare_for_battle()


    @property
    def not_finished(self):
        someone_dead = (self.tori.check_death()) or (self.uke.check_death())
        return (self.rnd < 100) and not (someone_dead)

    def run(self):
        sequences = []
        while self.not_finished:
            self.rnd += 1
            round = CombatRound(self)
            if self.rnd>1:
                round.flush()
            round.run()
            sequences.append(round.round_summary)
            round.flush()
            del round
        res = {'pub_date':self.pub_date,'rounds':sequences}
        return res

class CombatRound:
    def __init__(self,duel):
        self.duel = duel
        self.number = self.duel.rnd

    def flush(self):
        self.duel.tori.round_data['Narrative'] = []
        self.duel.uke.round_data['Narrative'] = []

    @property
    def round_summary(self):
        data = {}
        data['number'] = self.number
        if self.duel.tori.round_data['Initiative'] <= self.duel.uke.round_data['Initiative']:
            data['attacker'] = copy.deepcopy(self.duel.uke.round_data)
            data['defender'] = copy.deepcopy(self.duel.tori.round_data)
        else:
            data['attacker'] = copy.deepcopy(self.duel.tori.round_data)
            data['defender'] = copy.deepcopy(self.duel.uke.round_data)
        return data

    def run(self):
        self.declaration_phase()
        self.initiative_phase()
        self.resolution_phase()

    def declaration_phase(self):
        self.duel.tori.choose_attack()
        self.duel.uke.choose_attack()

    def initiative_phase(self):
        self.duel.tori.initiative_roll()
        self.duel.uke.initiative_roll()

    def resolution_phase(self):
        if self.duel.tori.round_data['Initiative'] > self.duel.uke.round_data['Initiative']:
            self.duel.tori.roll_attack(self.duel.uke)
            self.duel.uke.absorb_punishment(self.duel.tori)
            if self.duel.not_finished:
                self.duel.uke.roll_attack(self.duel.tori)
                self.duel.tori.absorb_punishment(self.duel.uke)
        else:
            self.duel.uke.roll_attack(self.duel.tori)
            self.duel.tori.absorb_punishment(self.duel.uke)
            if self.duel.not_finished:
                self.duel.tori.roll_attack(self.duel.uke)
                self.duel.uke.absorb_punishment(self.duel.tori)
