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
from django.http import JsonResponse
from collector.utils.basic import slug_decode
import logging

logger = logging.getLogger(__name__)


def run_duel(request, slug=None):
    slug = slug_decode(slug)
    try:
        pks = slug.split('_')
        attacker = pks[0]
        defender = pks[1]
    except:
        attacker = 0
        defender = 0
    if attacker == defender:
        attackers = Character.objects.filter(fencing_league=True)
        a = roll(attackers.count()) - 1
        attacker = attackers[a].id
        defenders = Character.objects.filter(fencing_league=True).exclude(id=attacker)
        d = roll(defenders.count()) - 1
        defender = defenders[d].id
    tori = Character.objects.get(pk=attacker)
    uke = Character.objects.get(pk=defender)
    duel = Duel(tori, uke)
    duel_data = duel.run()
    tori.save()
    uke.save()
    del duel

    context = {'duel_data': duel_data}
    template = get_template('optimizer/duel.html')
    html = template.render(context)
    c = {'mosaic': html}
    return JsonResponse(c)


def run_100_duels(request, slug=None):
    slug = slug_decode(slug)
    try:
        pks = slug.split('_')
        attacker = pks[0]
        defender = pks[1]
    except:
        attacker = 0
        defender = 0
    if attacker == defender:
        attackers = Character.objects.filter(fencing_league=True)
        a = roll(attackers.count()) - 1
        attacker = attackers[a].id
        defenders = Character.objects.filter(fencing_league=True).exclude(id=attacker)
        d = roll(defenders.count()) - 1
        defender = defenders[d].id
    tori = Character.objects.get(pk=attacker)
    uke = Character.objects.get(pk=defender)
    stats = [0, 0]
    for i in range(100):
        duel = Duel(tori, uke)
        _ = duel.run()
        if duel.winner == tori:
            stats[0] += 1
        else:
            stats[1] += 1
        del duel
        logger.info(stats)
    tori.save()
    uke.save()
    context = {'c': {'tori': tori.full_name, 'uke': uke.full_name, 'tori_score': stats[0], 'uke_score': stats[1],
                     'tori_color': tori.color, 'uke_color': uke.color}}
    template = get_template('optimizer/match_score.html')
    html = template.render(context)
    c = {'mosaic': html}
    return JsonResponse(c)


def run_fencing_tournament(request):
    import random
    logger.info("Starting Fencing tournament")
    contestants = Character.objects.filter(fencing_league=True)
    duel_victories = {}
    duel_fights = {}
    for x in contestants:
        logger.info("%s (%d) is joining the fencing tournament !" % (x.full_name, x.id))
        x.victory_rating = 0
        x.victories = 0
        x.fights = 0
        x.save()
        duel_victories[x.rid] = 0
        duel_fights[x.rid] = 0
    duel_data = []
    stats = []
    stat = []
    # fencers = copy.deepcopy(contestants)
    fencers = random.sample(list(contestants), 10)
    for uke in fencers:
        first_match = True
        for tori in fencers:
            if tori != uke:
                stat = [0, 0]
                for i in range(1):
                    duel = Duel(tori, uke)
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
                    stats.append(
                        {'tori': tori.full_name, 'tori_score': stat[0], 'uke': uke.full_name, 'uke_score': stat[1],
                         'tori_color': tori_color, 'uke_color': uke_color, "split": first_match})
                    if first_match == True:
                        first_match = False
                    del duel
    summary = []
    for x in fencers:
        if (x.victories > 0):
            x.victories = duel_victories[x.rid]
            x.fights = duel_fights[x.rid]
            x.victory_rating = math.ceil((x.victories * 100 / x.fights * 100)) / 100
            x.save()
    for x in fencers.order_by('-victories'):
        su = {'name': x.full_name, 'color': x.color, 'victories': duel_victories[x.rid], 'fights': duel_fights[x.rid]}
        summary.append(su)
    context = {'tournament_data': stats, 'summary': summary}
    template = get_template('optimizer/fencing_tournament.html')
    html = template.render(context)
    logger.info("Fencing tournament is over")
    c = {'mosaic': html}
    return JsonResponse(c)


def run_imperial_tournament(request):
    import math, random, copy
    fights = 7
    logger.info("Starting Fencing tournament")
    contestants = Character.objects.filter(fencing_league=True)
    duel_victories = {}
    duel_fights = {}
    number_of_participants = pow(2, round(math.sqrt(len(contestants))) - 1)
    for x in contestants:
        logger.info("%s (%d) is joining the imperial tournament !" % (x.full_name, x.id))
        x.victory_rating = 0
        x.victories = 0
        x.fights = 0
        x.save()
        duel_victories[x.rid] = 0
        duel_fights[x.rid] = 0

    fencers = copy.deepcopy(contestants)
    fencers = random.sample(list(fencers), number_of_participants)  # .sort(key=lambda s: s.full_name)
    duel_data = []
    tournament_data = []
    num_tier = math.sqrt(number_of_participants)
    while num_tier > 0:
        losers = []
        num_duel = 0

        # print(f'- Handling tier {int(num_tier)}')
        tier_results = {'tier': int(num_tier), 'duels': []}
        for i, v in enumerate(fencers):
            if i % 2 == 0:
                uke = v
            else:
                tori = v
                num_duel += 1
                stats = [0, 0]
                for f in range(fights):
                    duel = Duel(tori, uke)
                    d_data = duel.run()
                    duel_data.append(copy.deepcopy(d_data))
                    tori_color = '#444'
                    uke_color = '#444'
                    if duel.winner == tori:
                        stats[0] += 1
                    else:
                        stats[1] += 1
                if stats[0] > stats[1]:
                    losers.append(uke)
                    tori_color = tori.color
                    winner = tori
                else:
                    losers.append(tori)
                    uke_color = uke.color
                    winner = uke
                # print(f'  - Duel #{num_duel}: {tori.full_name} vs {uke.full_name} => {winner.full_name}')
                tier_results['duels'].append({'duel_id': f'ITDxT{int(num_tier)}xD{num_duel}x', 'tori': tori, 'uke': uke,
                                              'tori_color': tori_color, 'uke_color': uke_color, 'winner': winner,
                                              'scores': stats})
                del duel
        tournament_data.append(tier_results)
        for v in losers:
            fencers.remove(v)
        # print(f'Last fencers: {len(fencers)}')
        # print(f'{fencers}')
        num_tier -= 1
    context = {'tournament_data': tournament_data, 'character_items': contestants, "base_mark": 'contestant'}
    template = get_template('optimizer/imperial_tournament.html')
    html = template.render(context)
    logger.info("Fencing tournament is over")
    c = {'mosaic': html}
    return JsonResponse(c)
