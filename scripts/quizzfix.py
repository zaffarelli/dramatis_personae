""" Run things with: exec(open('scripts/quizzfix.py').read())
"""
from scenarist.models.quizz import QuizzAnswer

all = QuizzAnswer.objects.order_by('question', 'weight', 'name')
n = 1
q = None
for a in all:
    if q != a.question:
        q = a.question
        n = 1
    a.num = n
    n = n+1
    a.save()




