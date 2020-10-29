""" Run things with: exec(open('scripts/quizzshow.py').read())
"""

from scenarist.models.quizz import Quizz
from scenarist.models.dramas import Drama
from scenarist.models.acts import Act

dramas = Drama.objects.all()
for a in dramas:
    if len(a.quizz_set.all()) == 0:
        q = Quizz()
        q.drama = a
    else:
        q = a.quizz_set.first()
    q.randomize()
    q.save()

acts = Act.objects.all()
for a in acts:
    if len(a.quizz_set.all()) == 0:
        q = Quizz()
        q.act = a
    else:
        q = a.quizz_set.first()
    q.randomize()
    q.save()





