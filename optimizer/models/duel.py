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
    def winner(self):
        tori_dead = self.tori.check_death()
        uke_dead = self.uke.check_death()
        if (tori_dead and not uke_dead):
            winner = self.uke
        elif (uke_dead and not tori_dead):
            winner = self.tori
        else:
            if self.tori.round_data["Initiative"]>self.uke.round_data["Initiative"]:
                winner = self.tori
            elif self.tori.round_data["Initiative"]<self.uke.round_data["Initiative"]:
                winner = self.uke
            else:
                winner = None
        return winner

    @property
    def not_finished(self):
        someone_dead = (self.tori.check_death()) or (self.uke.check_death())
        return (self.rnd < 500) and not (someone_dead)

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
        res = {'pub_date':self.pub_date,'winner':self.winner,'rounds':sequences}
        return res

    def validate(self):
        pass
        # self.tori.fights += 1
        # self.uke.fights += 1
        # if self.winner == self.tori:
        #     self.tori.victories += 1
        # elif self.winner == self.uke:
        #     self.uke.victories += 1
        # self.tori.victory_rating = int((self.tori.victories / self.tori.fights) * 100)
        # self.uke.victory_rating = int((self.uke.victories / self.uke.fights) * 100)
        #self.tori.save()
        #self.uke.save()
        # print("Validate ==> %-25s:%02d  | %-25s:%02d"%(self.tori.full_name,self.tori.victories, self.uke.full_name, self.uke.victories ))

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
