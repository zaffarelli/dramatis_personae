"""
╔╦╗╔═╗  ╔═╗┌─┐┌─┐┌┐┌┌─┐┬─┐┬┌─┐┌┬┐
 ║║╠═╝  ╚═╗│  ├┤ │││├─┤├┬┘│└─┐ │
═╩╝╩    ╚═╝└─┘└─┘┘└┘┴ ┴┴└─┴└─┘ ┴
"""
from scenarist.models.quizz import Quizz
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404


def quizz_reroll(request, quizz_id, question_num, tag):
    q = Quizz.objects.get(pk=quizz_id)
    x = -1
    if q:
        setattr(q,tag, q.roll_answer(question_num))
        q.save()
    return HttpResponse(f'{x}')
