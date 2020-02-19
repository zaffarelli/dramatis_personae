
from optimizer.models.duel import Duel
from collector.models.character import Character
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template.loader import get_template

def run_duel(request,pka=None,pkb=None):    
    tori = Character.objects.get(pk=pka)
    uke  = Character.objects.get(pk=pkb)
    duel = Duel(tori,uke)
    duel_data = duel.run()
    context = {'duel_data': duel_data}
    template = get_template('optimizer/duel.html')
    html = template.render(context)
    return HttpResponse(html, content_type='text/html')
