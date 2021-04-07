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
        # print(f'New duel is : {tori.full_name} vs {uke.full_name}')
        self.pub_date = datetime.now()
        self.tori.prepare_for_battle()
        self.uke.prepare_for_battle()
        self.initial_tori = copy.deepcopy(self.tori.round_data)
        self.initial_uke = copy.deepcopy(self.uke.round_data)

    @property
    def winner(self):
        tori_dead = self.tori.check_death(self.uke)
        uke_dead = self.uke.check_death(self.tori)
        if (tori_dead and not uke_dead):
            winner = self.uke
        elif (uke_dead and not tori_dead):
            winner = self.tori
        else:
            if self.tori.peek('initiative')>self.uke.peek('initiative'):
                winner = self.tori
            elif self.tori.peek('initiative')<self.uke.peek('initiative'):
                winner = self.uke
            else:
                winner = None
        return winner

    @property
    def not_finished(self):
        someone_dead = (self.tori.check_death(self.uke)) or (self.uke.check_death(self.tori))
        return (self.rnd < 100) and not (someone_dead)

    def run(self):
        sequences = []

        while self.not_finished:
            self.rnd += 1
            round = CombatRound(self)
            round.run()
            sequences.append(round.round_summary)
            round.flush()
            del round
        res = {'pub_date':self.pub_date,'winner':self.winner,'rounds':sequences, 'amount':len(sequences), 'tori':self.initial_tori, 'uke':self.initial_uke}
        return res

class CombatRound:
    def __init__(self,duel):
        self.duel = duel
        self.number = self.duel.rnd

    def flush(self):
        self.duel.tori.round_data['narrative'] = []
        self.duel.uke.round_data['narrative'] = []

    @property
    def round_summary(self):
        data = {}
        data['number'] = self.number
        if self.duel.tori.peek('initiative') <= self.duel.uke.peek('initiative'):
            data['attacker'] = copy.deepcopy(self.duel.uke.round_data)
            data['defender'] = copy.deepcopy(self.duel.tori.round_data)
            data['joined_narrative'] = []
            i = 0
            for i in range(len(self.duel.tori.round_data['narrative'])):
                h = {'id':i}
                h['attacker'] = data['attacker']['narrative'][i]
                h['defender'] = data['defender']['narrative'][i]
                data['joined_narrative'].append(h)
        else:
            data['attacker'] = copy.deepcopy(self.duel.tori.round_data)
            data['defender'] = copy.deepcopy(self.duel.uke.round_data)
            data['joined_narrative'] = []
            for i in range(len(self.duel.tori.peek('narrative'))):
                h = {'id':i}
                h['attacker'] = data['attacker']['narrative'][i]
                h['defender'] = data['defender']['narrative'][i]
                data['joined_narrative'].append(h)
        return data

    def run(self):
        self.declaration_phase()
        self.initiative_phase()
        self.resolution_phase()

    def declaration_phase(self):
        self.duel.tori.choose_attack(self.duel.uke)
        self.duel.uke.choose_attack(self.duel.tori)

    def initiative_phase(self):
        self.duel.tori.initiative_roll(self.number)
        self.duel.uke.initiative_roll(self.number)

    def resolution_phase(self):
        max_attacks = max([self.duel.tori.peek('number_of_attacks'),self.duel.uke.peek('number_of_attacks')])
        if self.duel.tori.peek('initiative') > self.duel.uke.peek('initiative'):
            while max_attacks>0:
                if not self.duel.not_finished:
                    break
                self.duel.tori.roll_attack(self.duel.uke)
                self.duel.uke.absorb_punishment(self.duel.tori)
                if self.duel.not_finished:
                    self.duel.uke.roll_attack(self.duel.tori)
                    self.duel.tori.absorb_punishment(self.duel.uke)
                max_attacks = max([self.duel.tori.peek('number_of_attacks'),self.duel.uke.peek('number_of_attacks')])
        else:
            while max_attacks>0:
                if not self.duel.not_finished:
                    break
                self.duel.uke.roll_attack(self.duel.tori)
                self.duel.tori.absorb_punishment(self.duel.uke)
                if self.duel.not_finished:
                    self.duel.tori.roll_attack(self.duel.uke)
                    self.duel.uke.absorb_punishment(self.duel.tori)
                max_attacks = max([self.duel.tori.peek('number_of_attacks'),self.duel.uke.peek('number_of_attacks')])
