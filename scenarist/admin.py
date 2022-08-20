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
from scenarist.models.schemes import Scheme, SchemeAdmin
from scenarist.models.adventures import Adventure, AdventureAdmin
from scenarist.models.backlogs import Backlog, BacklogAdmin
from scenarist.models.scenes import Scene, SceneAdmin
from scenarist.models.quizz import QuizzQuestion, QuizzQuestionAdmin, QuizzAnswer, QuizzAnswerAdmin, Quizz, QuizzAdmin

admin.site.register(Epic, EpicAdmin)
admin.site.register(Drama, DramaAdmin)
admin.site.register(Act, ActAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Scheme, SchemeAdmin)
admin.site.register(Adventure, AdventureAdmin)
admin.site.register(Backlog, BacklogAdmin)
admin.site.register(Scene, SceneAdmin)
# admin.site.register(QuizzQuestion, QuizzQuestionAdmin)
# admin.site.register(QuizzAnswer, QuizzAnswerAdmin)
# admin.site.register(Quizz, QuizzAdmin)
