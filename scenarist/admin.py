'''
╔╦╗╔═╗  ╔═╗┌─┐┌─┐┌┐┌┌─┐┬─┐┬┌─┐┌┬┐
 ║║╠═╝  ╚═╗│  ├┤ │││├─┤├┬┘│└─┐ │ 
═╩╝╩    ╚═╝└─┘└─┘┘└┘┴ ┴┴└─┴└─┘ ┴ 
'''
from django.contrib import admin

from scenarist.models.epics import Epic, EpicAdmin
from scenarist.models.dramas import Drama, DramaAdmin
from scenarist.models.acts import Act, ActAdmin
from scenarist.models.events import Event, EventAdmin
from scenarist.models.quizz import QuizzQuestion, QuizzQuestionAdmin, QuizzAnswer, QuizzAnswerAdmin, Quizz, QuizzAdmin

admin.site.register(Epic, EpicAdmin)
admin.site.register(Drama, DramaAdmin)
admin.site.register(Act, ActAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(QuizzQuestion, QuizzQuestionAdmin)
admin.site.register(QuizzAnswer, QuizzAnswerAdmin)
admin.site.register(Quizz, QuizzAdmin)
