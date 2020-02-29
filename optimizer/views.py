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

def run_duel(request,pka=None,pkb=None):
    tori = Character.objects.get(pk=pka)
    uke  = Character.objects.get(pk=pkb)
    duel = Duel(tori,uke)
    duel_data = duel.run()
    duel.validate()
    tori.save()
    uke.save()
    context = {'duel_data': duel_data}
    template = get_template('optimizer/duel.html')
    html = template.render(context)
    return HttpResponse(html, content_type='text/html')

def run_100_duels(request,pka=None,pkb=None):
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
        duel.validate()
        del duel
        print(stats)
    tori.save()
    uke.save()
    return HttpResponse("<div class='classyview'><h2>After 100 duels...</h2><center><table class='duels'><tr><th style='background-color:%s;'>%s (%d)</th></tr><tr><td>%d</td></tr></table><table class='duels'><tr><th style='background-color:%s;'>%s (%d)</th></tr><tr><td>%d</td></tr></table></center></div>"%(tori.color,tori.full_name,tori.id,stats[0],uke.color,uke.full_name,uke.id,stats[1]), content_type='text/html')

def run_fencing_tournament(request):
    contestants = Character.objects.filter(fencing_league=True, balanced=True)
    duel_victories = {}
    duel_fights = {}
    for x in contestants:
        print("%s (%d) is joining the fencing tournament !"%(x.full_name,x.id))
        x.victory_rating = 0
        x.victories = 0
        x.fights = 0
        x.save()
        v = x.get_skill('Melee')
        w = x.get_weapon('MELEE').weapon_ref.weapon_accuracy
        a = x.get_armor().armor_ref.encumbrance
        if w==None:
            print("       No melee weapon!!!")
            return HttpResponse(status=204)
        else:
            print('        REF + Melee + WA - ENC = %d + %d + %d - %d = %d'%(x.PA_REF,v,w,a,x.PA_REF+v+w-a))
        duel_victories[x.rid]=0
        duel_fights[x.rid]=0
    duel_data = []
    stats = []
    stat = []


    for uke in contestants:
        first_match = True
        for tori in contestants.exclude(rid=uke.rid):
            stat = [0,0]
            print("---> Starting match: %s -vs- %s"%(uke.full_name,tori.full_name))
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
                print("---> Match is over: %s"%(winner))
                stats.append({'tori':tori.full_name,'tori_score':stat[0],'uke':uke.full_name,'uke_score':stat[1],'tori_color':tori_color,'uke_color':uke_color, "split":first_match})
                if first_match == True:
                    first_match = False
                #duel.validate()
                del duel
            #tori.save()
        #uke.save()
#    for x in contestants:
#        x.save()
    summary = []
    for x in contestants:
        x.victories = duel_victories[x.rid]
        x.fights = duel_fights[x.rid]
        x.victory_rating = int((x.victories / x.fights) * 100)
        x.save()
    for x in contestants.order_by('-victories'):
        su = { 'name':x.full_name,'color': x.color,'victories': duel_victories[x.rid],'fights':duel_fights[x.rid]}
        summary.append(su)
    print("---> Summary shot")
    print(summary)
    context = {'tournament_data': stats, 'summary':summary}
    template = get_template('optimizer/fencing_tournament.html')
    html = template.render(context)
    return HttpResponse(html, content_type='text/html')
