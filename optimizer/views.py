'''
╔╦╗╔═╗  ╔═╗┌─┐┌┬┐┬┌┬┐┬┌─┐┌─┐┬─┐
 ║║╠═╝  ║ ║├─┘ │ │││││┌─┘├┤ ├┬┘
═╩╝╩    ╚═╝┴   ┴ ┴┴ ┴┴└─┘└─┘┴└─
'''
from optimizer.models.duel import Duel
from collector.models.character import Character
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template.loader import get_template
import copy
import math
from collector.utils.fs_fics7 import roll

import logging
logger = logging.getLogger(__name__)

def run_duel(request,pka=None,pkb=None):
    if pka==pkb:
        attackers = Character.objects.filter(fencing_league=True)
        a = roll(attackers.count())-1
        attacker = attackers[a].id
        print(f'Attacker: {pka}')
        defenders = Character.objects.filter(fencing_league=True).exclude(id=attacker)
        d = roll(defenders.count())-1
        defender = defenders[d].id
        print(f'Defender: {defender}')

    tori = Character.objects.get(pk=attacker)
    uke  = Character.objects.get(pk=defender)
    duel = Duel(tori,uke)
    duel_data = duel.run()
    tori.save()
    uke.save()
    del duel
    
    context = {'duel_data': duel_data}
    template = get_template('optimizer/duel.html')
    html = template.render(context)
    return HttpResponse(html, content_type='text/html')

def run_100_duels(request,pka=None,pkb=None):
    if pka==pkb:
        fencers = Character.objects.filter(fencing_league=True)
        x = roll(fencers.count())-1
        print(x)
        pka = fencers[x].id
        fencers2 = Character.objects.filter(fencing_league=True).exclude(id=pka)
        y = roll(fencers2.count())-1
        print(y)
        pkb = fencers2[y].id
    tori = Character.objects.get(pk=pka)
    uke  = Character.objects.get(pk=pkb)
    stats = [0,0]
    for i in range(100):
        duel = Duel(tori,uke)
        duel_data = duel.run()
        if duel.winner == tori:
            stats[0] += 1
        else:
            stats[1] += 1
        del duel
        logger.info(stats)
    tori.save()
    uke.save()
    context = {'c':{'tori':tori.full_name,'uke':uke.full_name,'tori_score':stats[0],'uke_score':stats[1],'tori_color':tori.color,'uke_color':uke.color}}
    template = get_template('optimizer/match_score.html')
    html = template.render(context)
    return HttpResponse(html, content_type='text/html')

def run_fencing_tournament(request):
    logger.info("Starting Fencing tournament")
    contestants = Character.objects.filter(fencing_league=True)
    duel_victories = {}
    duel_fights = {}
    for x in contestants:
        logger.info("%s (%d) is joining the fencing tournament !"%(x.full_name,x.id))
        x.victory_rating = 0
        x.victories = 0
        x.fights = 0
        x.save()
        duel_victories[x.rid]=0
        duel_fights[x.rid]=0
    duel_data = []
    stats = []
    stat = []
    for uke in contestants:
        first_match = True
        for tori in contestants.exclude(rid=uke.rid):
            stat = [0,0]
            for i in range(1):
                duel = Duel(tori,uke)
                d_data = duel.run()
                duel_data.append(copy.deepcopy(d_data))
                tori_color = '#444'
                uke_color = '#444'
                duel_fights[duel.tori.rid] += 1
                duel_fights[duel.uke.rid] += 1
                if duel.winner == tori:
                    stat[0] += 1
                    winner = duel.winner.full_name
                    duel_victories[duel.winner.rid] += 1
                    tori_color = tori.color
                elif duel.winner == uke:
                    stat[1] += 1
                    winner = duel.winner.full_name
                    duel_victories[duel.winner.rid] += 1
                    uke_color = uke.color
                else:
                    winner = 'draw'
                stats.append({'tori':tori.full_name,'tori_score':stat[0],'uke':uke.full_name,'uke_score':stat[1],'tori_color':tori_color,'uke_color':uke_color, "split":first_match})
                if first_match == True:
                    first_match = False
                del duel
    summary = []
    for x in contestants:
        x.victories = duel_victories[x.rid]
        x.fights = duel_fights[x.rid]
        x.victory_rating = math.ceil((x.victories*100 / x.fights*100) )/100
        x.save()
    for x in contestants.order_by('-victories'):
        su = { 'name':x.full_name,'color': x.color,'victories': duel_victories[x.rid],'fights':duel_fights[x.rid]}
        summary.append(su)
    context = {'tournament_data': stats, 'summary':summary}
    template = get_template('optimizer/fencing_tournament.html')
    html = template.render(context)
    logger.info("Fencing tournament is over")
    return HttpResponse(html, content_type='text/html')
