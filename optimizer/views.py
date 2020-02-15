
from optimizer.models.duel import Duel
from collector.models.character import Character
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template.loader import get_template

def run_duel(request,pka=None,pkb=None):
    duel = Duel()
    duel.tori = get_object_or_404(Character,pk=pka)
    print(duel.tori.full_name)
    duel.uke  = get_object_or_404(Character,pk=pkb)
    print(duel.uke.full_name)
    duel.save()
    duel_data = duel.run()
    duel.save()
    context = {'duel_data': duel_data}
    template = get_template('optimizer/duel.html')
    html = template.render(context)
    return HttpResponse(html, content_type='text/html')
